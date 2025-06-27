FROM jupyter/pyspark-notebook:spark-3.5.0

USER root

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install --upgrade pip && \
    grep -v "rpy2" requirements.txt > /app/temp_requirements.txt && \
    pip install -r /app/temp_requirements.txt

CMD [ "bash" ]
