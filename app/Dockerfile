FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

ADD ./app /home/app/
WORKDIR /home/app/

EXPOSE 5000

RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]
