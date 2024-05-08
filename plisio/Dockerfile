FROM python:3.12
LABEL authors="RuVl_13"

# Update packages
RUN apt-get update && apt-get upgrade -y

# Set enviroment variables
ENV TZ Europe/Moscow
ENV PIP_ROOT_USER_ACTION=ignore

# Prepare project directory
CMD mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

# Copy and install requirements (docker trick)
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project to directory
COPY . ./

# Run api
ENTRYPOINT uvicorn api.main:app --host 0.0.0.0 --port 8000 --proxy-headers
