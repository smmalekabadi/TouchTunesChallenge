import os
import requests
from datetime import datetime, timedelta
from prettytable import PrettyTable
from dotenv import load_dotenv
from configparser import ConfigParser

NUMBER_OF_HAZARDOUS_ASTEROID = 3
NUMBER_OF_DAY_RANGE = 7


def get_asteroid_data(start_date, end_date):
    r = None
    try:
        r = requests.get(
            'https://api.nasa.gov/neo/rest/v1/feed?start_date=' + start_date + '&end_date=' + end_date + '&api_key=' +
            os.getenv("API_KEY"),
            headers={'Accept': 'application/json'})
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"Status Code: {r.status_code}, Content: {r.json()}")
        exit(1)
    response_json = r.json()
    return response_json


def create_asteroid_data_table(start_date="2019-10-31", end_date="2019-11-02"):
    response_json = get_asteroid_data(start_date, end_date)
    table = PrettyTable(['name', 'id', 'close_approach_date_full'])
    for z in response_json["near_earth_objects"]:
        for x in response_json["near_earth_objects"][z]:
            for y in x['close_approach_data']:
                table.add_row([x['name'], x['id'], y['close_approach_date_full']])
    print(table)


def calculate_velocities(start_date="2020-09-10",
                         end_date="2020-09-17"):
    response_json = get_asteroid_data(start_date, end_date)
    min_veloc = 300_000_000.0
    max_veloc = 0.0
    count = 0
    sum = 0
    speeds = []
    median = 0
    for z in response_json["near_earth_objects"]:
        for x in response_json["near_earth_objects"][z]:
            for y in x['close_approach_data']:
                min_veloc = min(float(y['relative_velocity']['kilometers_per_second']), min_veloc)
                max_veloc = max(float(y['relative_velocity']['kilometers_per_second']), max_veloc)
                sum += float(y['relative_velocity']['kilometers_per_second'])
                count += 1
                speeds.append(float(y['relative_velocity']['kilometers_per_second']))
    speeds.sort()
    if count % 2 == 0:
        median = speeds[int((count + 1) / 2)]
    else:
        median = (speeds[int(count / 2)] + speeds[int((count + 1) / 2)]) / 2

    table = PrettyTable(['slowest', 'fastest', 'mean', 'median'])
    table.add_row([min_veloc, max_veloc, sum / count, median])
    print(table)
    return min_veloc, max_veloc, sum / count, median


def recent_hazardous_asteroid(count=NUMBER_OF_HAZARDOUS_ASTEROID):
    counter = 0
    end_date = datetime.now()
    start_date = end_date - timedelta(days=NUMBER_OF_DAY_RANGE)
    table = PrettyTable(['name', 'id', 'close_approach_date_full', 'is_potentially_hazardous_asteroid'])
    while counter < count:
        date_start_str = start_date.strftime('%Y-%m-%d')
        date_end_str = end_date.strftime('%Y-%m-%d')
        response_json = get_asteroid_data(date_start_str, date_end_str)

        for z in response_json["near_earth_objects"]:
            for x in response_json["near_earth_objects"][z]:
                if bool(x['is_potentially_hazardous_asteroid']) and counter < count:
                    for y in x['close_approach_data']:
                        table.add_row(
                            [x['name'], x['id'], y['close_approach_date_full'], x['is_potentially_hazardous_asteroid']])

                    counter += 1

        if counter < count:
            end_date = start_date
            start_date = start_date - timedelta(days=NUMBER_OF_DAY_RANGE)
    print(table)


def configure():
    load_dotenv()
    config_object = ConfigParser()
    config_object.read("config.ini")
    service_info = config_object['service']
    return service_info


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    service_info = configure()
    print(f"\t\t\tTable of Near Of Earth Asteroid")
    create_asteroid_data_table(service_info['start_date_asteroid'], service_info['end_date_asteroid'])
    print(f"\t\t\tTable of Velocity of fastest, slowest, mean and media")
    calculate_velocities(service_info['start_date_velocities'], service_info['end_date_velocities'])
    print(f"\n\n\t\t\t\tTable of Near Of Earth Asteroid which potentially hazardous")
    recent_hazardous_asteroid(int(service_info['number_of_hazardous_asteroid']))