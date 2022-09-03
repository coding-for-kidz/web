# 1
FROM python:3.10-slim

# 2
WORKDIR /usr/src/

# 3
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# 4
# requirements
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r requirements.txt

# 5
COPY . /usr/src/services/web/
COPY docker_run.py /usr/src/
COPY docker-run.sh /usr/src/
COPY config.cfg /usr/src/
# 6
ENTRYPOINT ["sh", "docker-run.sh"]
