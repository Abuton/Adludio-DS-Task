# To enable ssh & remote debugging on app service change the base image to the one below
FROM python:3.7

RUN apt-get update -y
RUN apt-get install apt-utils bash gcc htop -y
RUN apt-get install -y build-essential python3-pip python3-dev 
RUN apt-get install -y cmake libboost-all-dev

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app
COPY data /app/data
COPY lib /app/lib
COPY templates /app/templates
COPY test /app/test

RUN export LC_ALL=en_US.UTF-8
RUN export LANG=en_US.UTF-8

EXPOSE 80

ENTRYPOINT [ "/bin/bash", "-c"]
CMD ["exec python app.py"]