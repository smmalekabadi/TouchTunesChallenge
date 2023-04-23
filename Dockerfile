FROM python:latest
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD config.ini /
ADD main.py /
CMD [ "python", "./main.py" ]