# Kafka Broker

Follow these instructions to install Kafka broker.

Create Ubuntu 18.04 VM with 2vCPUs 8GB RAM 50 GB disk

The below instructions are taken from [kafka-docker readme](https://github.com/wurstmeister/kafka-docker/blob/master/README.md)

## Install

### docker-compose

Install docker-compose via: https://docs.docker.com/compose/install/

### kafka broker

Clone repository

```
git clone https://github.com/wurstmeister/kafka-docker.git
cd kafka-docker
```

Edit `docker-compose.yml` to contain the below

**Note:** `KAFKA_ADVERTISED_HOST_NAME` should be set to the external ipaddress of the VM

```
version: '2'
services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
  kafka:
    build: .
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_HOST_NAME: 172.28.3.196
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

Provision kafka/zookeeper

```
docker-compose up -d
```

## Usage

Log into kafka container (replace with your container id)

```
sudo docker exec -it 4745f6478787  /bin/bash
```

### Publish message on on topic

Run the below command (taken from [kafka-quickstart](https://kafka.apache.org/quickstart))

```
/opt/kafka/bin/kafka-console-producer.sh --topic <topic name> --bootstrap-server localhost:9092
```

Terminate with `^C`

### Consume maessage from topic

Run the below command (taken from [kafka-quickstart](https://kafka.apache.org/quickstart))

```
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic <topic name> --from-beginning
```

### Create topics

```
/opt/kafka/bin/kafka-topics.sh --create --topic <topic name> --bootstrap-server localhost:9092
```

### List topics

```
/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Delete topic

```
/opt/kafka/bin/kafka-topics.sh --delete --topic <topic name> --bootstrap-server localhost:9092
```
