# Datalake

**TEMP README**

Datalake services run on kubernetes. You can use [these instructions](https://github.com/5GZORRO/infrastructure/blob/master/docs/kubernetes.md) to provision such a one

## Pre-requisites

* Ensure you have kafka broker already installed. You can use [these instructions](https://github.com/5GZORRO/infrastructure/blob/master/docs/kafka.md) to provision such a one
* Install argo and argo-events per [these instructions](https://github.com/5GZORRO/issm/blob/master/docs/argo.md)

## Run the services

Log into kubernetes master

```
cd ~
git clone https://github.com/5GZORRO/datalake.git
cd datalake
git checkout ingest_pipeline2
```

### Build

```
docker build -t swagger_server .
```

### Run

```
export KUBE_PATH_NAME=${HOME}/.kube
```

Update kafka url accordingly

```
docker run -v ${KUBE_PATH_NAME}:/root/.kube -p 8080:8080 \
  --env KUBERNETES_URL='127.0.0.1:8443' \
  --env KAFKA_URL='172.15.0.195:9092' \
  --env S3_URL='127.0.0.1:9000' \
  --env S3_ACCESS_KEY='user' \
  --env S3_SECRETE_KEY='password' \
  swagger_server
```

### Create user

```
cd ~/datalake/experiments
./makeuser.sh operator-a
```