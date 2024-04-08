FROM python:3.10
LABEL authors="RuVl_13"

# Update packages
RUN apt-get update && apt-get upgrade -y

# Prepare project directory
CMD mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

# Copy project to directory
COPY . /usr/src/app/

# Set enviroment variables
ENV TZ Europe/Moscow
ENV PIP_ROOT_USER_ACTION=ignore

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Compile languages
RUN pybabel compile -d core/text/locales -D telegram

# Run app
ENTRYPOINT python3 run.py
