FROM ubuntu:19.10

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev


RUN apt-get install -y python3 python3-pip

RUN pip3 install jsonpickle && \
pip3 install flask && \
pip3 install flask-cors && \ 
pip3 install pandas

RUN apt-get install git -y

WORKDIR /app

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "server.py" ]