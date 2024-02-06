FROM python:3.11.1
ADD . /datalake
WORKDIR /datalake

# JAVA (PySpark)
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

RUN pip install -r requirements.txt
CMD ["python", "-m", "flask", "--app", "api", "run", "--host=0.0.0.0"]