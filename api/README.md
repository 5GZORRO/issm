# issm-api

## Deploy the service

Log into kuberneters master where ISSM is installed

Invoke the below in this order

**Note:**

1. you may need to update below settings according to your environment

1. deployment uses myregistrykey secrete to pull image from private docker registry. Refer [here](https://github.com/5GZORRO/infrastructure/blob/master/docs/kubernetes-private-dockerregistry.md) to set it up

1. ensure to create the secrete in `argo-events` namespace

```
export REGISTRY=docker.pkg.github.com
export IMAGE=$REGISTRY/5gzorro/issm/issm-api

export ISSM_KAFKA_HOST=172.15.0.195
export ISSM_KAFKA_PORT=9092
```

```
envsubst < deploy/deployment.yaml.template | kubectl apply -f -
kubectl apply -f deploy/service.yaml
```

## API

Submit slice intent to ISSM kafka bus

```
curl -H "Content-type: application/json" -POST -d '{"service_owner": "<service_owner>", "intent": {.., "qos_parameters": {..}}}' https://issm_api_ip_address:8080/instantiate

REST path:
    issm_api_ip_address - ipaddress ISSM API service.

Data payload:
    service_owner - the service owner/tenant to perform this request (str)
    intent        - the intent to be submitted (json - TBD)

Return:
    status - 200
    transaction_uuid - the transaction uuid of this business flow instance
```

## Build (**relevant for developers only**)

1.  Set the `REGISTRY` environment variable to hold the name of your docker registry. The following command sets it
    equal to the docker github package repository.

    ```
    $ export REGISTRY=docker.pkg.github.com
    ```

1.  Set the `IMAGE` environment variable to hold the image.

    ```
    $ export IMAGE=$REGISTRY/5gzorro/issm/issm-api
    ```

1.  Invoke the below command.

    ```
    $ docker build --tag "$IMAGE" --force-rm=true .
    ```

1.  Push the image.

    ```
    $ docker push "$IMAGE"
    ```
