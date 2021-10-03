FROM python:3
WORKDIR fast_api_project
COPY requirements.txt /fast_api_project/
RUN pip install -r requirements.txt
COPY . /fast_api_project/