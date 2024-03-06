FROM ubuntu:latest
WORKDIR /app
RUN apt update && apt install -y python3 python3-pip
RUN pip install flask gunicorn requests pandas numpy boto3
COPY ./ .
CMD gunicorn -w 5 -b 0.0.0.0:8000 app:app