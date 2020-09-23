# TODO
FROM nvcr.io/nvidia/pytorch:20.08-py3

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

FROM nginx:latest

EXPOSE 80