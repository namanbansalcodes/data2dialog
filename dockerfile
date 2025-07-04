FROM python:3

COPY . /code/

ENV PYTHONUNBUFFERED=1
ENV DOCKER_BUILDKIT=1

WORKDIR /code
COPY requirements.txt /code/

# run these commands
RUN pip install -r requirements.txt
