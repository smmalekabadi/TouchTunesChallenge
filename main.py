# hardcoded dates and test

import os

import requests
import json
from datetime import datetime, date, timedelta
from prettytable import PrettyTable
from dotenv import load_dotenv

NUMBER_OF_HAZARDOUS_ASTEROID = 3
NUMBER_OF_DAY_RANGE = 7


def get_asteroid_data(start_date, end_date):
    r = requests.get(
        'https://api.nasa.gov/neo/rest/v1/feed?start_date=' + start_date + '&end_date=' + end_date + '&api_key=' +
        os.getenv("API_KEY"),
        headers={'Accept': 'application/json'})
    # print(f"Status Code: {r.status_code}, Content: {r.json()}")
    response_json = r.json()
    return response_json


def create_table():
    start_date = date(2019, 10, 31)
    end_date = date(2019, 11, 2)
    date_start_str = start_date.strftime('%Y-%m-%d')
    date_end_str = end_date.strftime('%Y-%m-%d')
    response_json = get_asteroid_data(date_start_str, date_end_str)
    table = PrettyTable(['name', 'id', 'close_approach_date_full'])
    for z in response_json["near_earth_objects"]:
        for x in response_json["near_earth_objects"][z]:
            for y in x['close_approach_data']:
                table.add_row([x['name'], x['id'], y['close_approach_date_full']])
    print(table)


def calculate_velocities():
    start_date = date(2020, 9, 10)
    end_date = date(2020, 9, 17)
    date_start_str = start_date.strftime('%Y-%m-%d')
    date_end_str = end_date.strftime('%Y-%m-%d')
    response_json = get_asteroid_data(date_start_str, date_end_str)
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


def recent_hazardous_asteroid():
    count = 0

    end_date = datetime.now()
    start_date = end_date - timedelta(days=NUMBER_OF_DAY_RANGE)
    table = PrettyTable(['name', 'id', 'close_approach_date_full', 'is_potentially_hazardous_asteroid'])
    while count < NUMBER_OF_HAZARDOUS_ASTEROID:
        date_start_str = start_date.strftime('%Y-%m-%d')
        date_end_str = end_date.strftime('%Y-%m-%d')
        response_json = get_asteroid_data(date_start_str, date_end_str)

        for z in response_json["near_earth_objects"]:
            for x in response_json["near_earth_objects"][z]:
                if bool(x['is_potentially_hazardous_asteroid']) and count < NUMBER_OF_HAZARDOUS_ASTEROID:
                    for y in x['close_approach_data']:
                        table.add_row(
                            [x['name'], x['id'], y['close_approach_date_full'], x['is_potentially_hazardous_asteroid']])

                    count += 1

        if count < NUMBER_OF_HAZARDOUS_ASTEROID:
            end_date = start_date
            start_date = start_date - timedelta(days=NUMBER_OF_DAY_RANGE)
    print(table)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()
    print(f"\t\t\ttable of Near Of Earth Asteroid")
    create_table()
    print(f"\n\n\t table of Velocity of fastest, slowest, mean and median ")
    calculate_velocities()
    print(f"\n\n\t\t\t\ttable of Near Of Earth Asteroid which potentially hazardous")
    recent_hazardous_asteroid()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
