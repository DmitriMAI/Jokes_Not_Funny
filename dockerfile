FROM continuumio/miniconda3

COPY . .

RUN conda install python=3.8 pytorch cudatoolkit -c pytorch

RUN apt-get update

RUN apt-get install -y openjdk-11-jdk

RUN pip install -U aiogram

RUN pip install transformers tensorflow

RUN pip install python-dotenv

RUN pip install kafka-python

ADD https://dlcdn.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz ./

RUN tar -xzf kafka_2.13-3.3.1.tgz
