FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

COPY ./app /home/app/
WORKDIR /home/app/

EXPOSE 5000

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]
