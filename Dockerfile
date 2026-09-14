FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y openjdk-21-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

WORKDIR /app

COPY credit_risk_small.csv /app/credit_risk_small.csv
COPY train_model.py /app/train_model.py

RUN pip install --no-cache-dir pyspark==4.2.0 pandas numpy

RUN mkdir -p /app/model

CMD ["python", "/app/train_model.py"]