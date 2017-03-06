FROM python:3.5.3-alpine
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ADD . /project
WORKDIR /project
RUN ["python", "manage.py", "migrate"]
RUN ["python", "manage.py", "loaddata", "fixtures/initial.json"]
