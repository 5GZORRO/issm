# issm-api

Component responsible for providing management API endpoint service for ISSM.

## Pre-requisites

issm-api calls into argo-server REST endpoints.

* Argo server is automatically installed with argo and is internally available within kubernetes
* Expose argo-server externally via these [instructions](https://argoproj.github.io/argo-workflows/argo-server/#expose-a-loadbalancer)

## Deploy the service

Log into 5GZorro platform kuberneters master (where ISSM platform is installed)

Invoke the below in this order

**Note:** you may need to update below settings according to your environment

```
export REGISTRY=docker.pkg.github.com
export IMAGE=$REGISTRY/5gzorro/issm/issm-api:d8ed311

export ISSM_KAFKA_HOST=172.28.3.196
export ISSM_KAFKA_PORT=9092

# cluster-IP
export ARGO_SERVER=10.43.204.81:2746

# externally accessed argo-server
export LB_ARGO_SERVER=172.28.3.42:32026
```

Deploy

```
envsubst < deploy/deployment.yaml.template | kubectl apply -n issm -f -
kubectl apply -f deploy/service.yaml -n issm
```

## API

### Submit slice intent

```
curl -H "Content-type: application/json" -POST -d "@/path/to/intent.json" http://issm_api_ip_address:30080/instantiate/<service_owner>
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
    transaction_uuid - the transaction uuid of this business flow instance (uuid)
```

Invocation example:

```
    curl -H "Content-type: application/json" -POST -d "@payloads/intent.json" http://172.28.3.42:30080/instantiate/operator-a

    {
        "transaction_uuid": "cc0bb0e0fe214705a9222b4582f17961"
    }
```

### List workflows ref

Returns list of transactions invoked by the service owner

```
curl -H "Content-type: application/json" -GET http://issm_api_ip_address:30080/get_workflows_ref/<service_owner>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner       - the id of the service owner/tenant that triggered the workflows (str)
```

Return:

```
    status - 200
    list of dictionaries (json):
        transaction_uuid - transaction uuid
        status - overall status of the transaction
        ref - launch-in-context URLs into Argo UI's service owner view
```

Invocation example:

```
    curl -H "Content-type: application/json" -GET http://172.28.3.42:30080/get_workflows/operator-a
    [
      {
        "transaction_uuid": "77a6dc4622374122917d4f001a1f2a0a",
        "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=77a6dc4622374122917d4f001a1f2a0a",
        "status": "Succeeded"
      },
      {
        "transaction_uuid": "d33a603ce1054143bd9def88729d0fa3",
        "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=d33a603ce1054143bd9def88729d0fa3",
        "status": "Failed"
      },
      {
        "transaction_uuid": "f40b12222a5a40c9bb2e961180077a98",
        "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=f40b12222a5a40c9bb2e961180077a98",
        "status": "Succeeded"
      },
      {
        "transaction_uuid": "e1642c75b5f947128cf8312d2aa46e23",
        "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=e1642c75b5f947128cf8312d2aa46e23",
        "status": "Succeeded"
      },
      {
        "transaction_uuid": "a5604bc8a00c495ebe8932d4e3ecec61",
        "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=a5604bc8a00c495ebe8932d4e3ecec61",
        "status": "Succeeded"
      }
    ]
```

## Build (**relevant for developers only**)

1.  Set the `REGISTRY` environment variable to hold the name of your docker registry. The following command sets it
    equal to the docker github package repository.

    ```
    $ export REGISTRY=docker.pkg.github.com
    ```

1.  Set the `IMAGE` environment variable to hold the image.

    ```
    $ export IMAGE=$REGISTRY/5gzorro/issm/issm-api:d8ed311
    ```

1.  Invoke the below command.

    ```
    $ docker build --tag "$IMAGE" --force-rm=true .
    ```

1.  Push the image.

    ```
    $ docker push "$IMAGE"
    ```
