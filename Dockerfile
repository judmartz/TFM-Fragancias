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

# Luego construye la imagen:
# docker build -t tfm-fragancias .

# Y lanza el contenedor:
# docker run -p 8888:8888 -v $(pwd):/app tfm-fragancias

# Después accede a Jupyter en tu navegador en http://localhost:8888 con el token que aparece en consola.
