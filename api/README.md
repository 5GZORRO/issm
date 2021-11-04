# issm-api

Component responsible for providing management API endpoint service for ISSM.

## Deploy the service

Log into kuberneters master where ISSM is installed

Invoke the below in this order

**Note:**

1. you may need to update below settings according to your environment

1. deployment uses myregistrykey secrete to pull image from private docker registry. Refer [here](https://github.com/5GZORRO/infrastructure/blob/master/docs/kubernetes-private-dockerregistry.md) to set it up

1. ensure to create the secrete in `issm` namespace

```
export REGISTRY=docker.pkg.github.com
export IMAGE=$REGISTRY/5gzorro/issm/issm-api:temp

export ISSM_KAFKA_HOST=172.28.3.196
export ISSM_KAFKA_PORT=9092
```

```
envsubst < deploy/deployment.yaml.template | kubectl apply -n issm -f -
kubectl apply -f deploy/service.yaml -n issm
```

## API

### Submit slice intent

```
curl -H "Content-type: application/json" -POST -d "@/path/to/intent.json" http://issm_api_ip_address:8080/instantiate/<service_owner>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner      - the id of the service owner/tenant to perform this request (str)
```

Data payload:

refer [here](payloads/intent.md) for current supported format

Return:

```
    status - 200
    transaction_uuid - the transaction uuid of this business flow instance
```

Invocation example:

```
    curl -H "Content-type: application/json" -POST -d "@payloads/intent.json" http://172.28.3.42:30080/instantiate/operator-a

    {
        "transaction_uuid": "cc0bb0e0fe214705a9222b4582f17961"
    }
```

## Build (**relevant for developers only**)

1.  Set the `REGISTRY` environment variable to hold the name of your docker registry. The following command sets it
    equal to the docker github package repository.

    ```
    $ export REGISTRY=docker.pkg.github.com
    ```

1.  Set the `IMAGE` environment variable to hold the image.

    ```
    $ export IMAGE=$REGISTRY/5gzorro/issm/issm-api:temp
    ```

1.  Invoke the below command.

    ```
    $ docker build --tag "$IMAGE" --force-rm=true .
    ```

1.  Push the image.

    ```
    $ docker push "$IMAGE"
    ```
