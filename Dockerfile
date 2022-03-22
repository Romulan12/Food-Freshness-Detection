FROM python:3.7.3

RUN python -m pip install --upgrade pip

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app/

RUN apt-get update  

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt 

COPY . /usr/src/app/

RUN chmod -R +777 /usr/src/app/

EXPOSE 60011

WORKDIR /usr/src/app/code/

CMD ["python3", "FreshnessDetection.py","--reload","--port","8046","--host","0.0.0.0"]

