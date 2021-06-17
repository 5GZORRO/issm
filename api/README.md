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
export IMAGE=$REGISTRY/5gzorro/issm/issm-api:8a4668a

export ISSM_KAFKA_HOST=172.28.3.196
export ISSM_KAFKA_PORT=9092
```

```
envsubst < deploy/deployment.yaml.template | kubectl apply -f -
kubectl apply -f deploy/service.yaml
```

## API

Submit slice intent to ISSM kafka bus

```
curl -H "Content-type: application/json" -POST -d '{"service_owner": "<service_owner>", "intent": {..}}' http://issm_api_ip_address:8080/instantiate

REST path:
    issm_api_ip_address - ipaddress ISSM API service.

Data payload:
    service_owner      - the id of the service owner/tenant to perform this request (str)
    intent             - the intent to be submitted (json)
        requested_price  - price of the resource (range e.g. "15-25")
        latitude       - the desired location of the slice/resource
        longitude      - the desired location of the slice/resource
        resource_type  - the type of the resource (e.g, "vnf")
        category       - category (e.g "cdn")
        qos_parameters - (json - e.g. {"bandwidth": "30"})

Return:
    status - 200
    transaction_uuid - the transaction uuid of this business flow instance
```

Invocation example:

```
curl -H "Content-type: application/json" -POST -d '{"service_owner": "operator-a", "intent": {"requested_price": "15-25", "latitude": "43", "longitude": "10", "resource_type": "vnf", "category": "cdn", "qos_parameters": {"bandwidth": "30"} }}' http://172.28.3.42:30080/instantiate

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
