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
export IMAGE=$REGISTRY/5gzorro/issm/issm-api:dfbbc7c

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

### Submit transaction (slice intent)

Submit a transaction for the given service owner

```
curl -H "Content-type: application/json" -POST -d "@/path/to/intent.json" http://issm_api_ip_address:30080/transactions/<service_owner>/<transaction_type>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner       - the service owner (str)
    transaction_type    - the type of the transaction to submit (e.g. scaleout)
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
    curl -H "Content-type: application/json" -POST -d "@payloads/intent.json" http://172.28.3.42:30080/transactions/operator-a/scaleout

    {
        "transaction_uuid": "cc0bb0e0fe214705a9222b4582f17961"
    }
```

### List transactions

Returns all transactions of the service owner

```
curl -H "Content-type: application/json" -GET http://issm_api_ip_address:30080/transactions/<service_owner>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner       - the service owner (str)
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
    curl -H "Content-type: application/json" -GET http://172.28.3.42:30080/transactions/operator-a
    [
      {
        "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=c5df607af95f469ca058919989968a33",
        "status": "Running",
        "transaction_type": "scaleout",
        "transaction_uuid": "c5df607af95f469ca058919989968a33"
      },
      {
        "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=a547d8726e7049b6bd7eee4cf3b93831",
        "status": "Succeeded",
        "transaction_type": "instantiate",
        "transaction_uuid": "a547d8726e7049b6bd7eee4cf3b93831"
      },
      {
        "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=6261754de98c4537ba08bd6b3c8d7d36",
        "status": "Succeeded",
        "transaction_type": "scaleout",
        "transaction_uuid": "6261754de98c4537ba08bd6b3c8d7d36"
      }
    ]
```

### List transactions from a given type

Returns transactions of a given type of the service owner

```
curl -H "Content-type: application/json" -GET http://issm_api_ip_address:30080/transactions/<service_owner>/<transaction_type>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner       - the service owner (str)
    transaction_type    - the type of the transaction (e.g. scaleout)
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
    curl -H "Content-type: application/json" -GET http://172.28.3.42:30080/transactions/operator-a/scaleout
    [
      {
        "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=c5df607af95f469ca058919989968a33",
        "status": "Running",
        "transaction_type": "scaleout",
        "transaction_uuid": "c5df607af95f469ca058919989968a33"
      },
      {
        "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=6261754de98c4537ba08bd6b3c8d7d36",
        "status": "Succeeded",
        "transaction_type": "scaleout",
        "transaction_uuid": "6261754de98c4537ba08bd6b3c8d7d36"
      }
    ]
```

### Delete transaction

Deletes a single transaction owned by the service owner

```
curl -H "Content-type: application/json" -X DELETE http://issm_api_ip_address:30080/transactions/<service_owner>/<transaction_uuid>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner       - the service owner (str)
    transaction_uuid    - the uuid of the transaction (str in uuid format)
```

Return:

```
    status - 200
```



## Build (**relevant for developers only**)

1.  Set the `REGISTRY` environment variable to hold the name of your docker registry. The following command sets it
    equal to the docker github package repository.

    ```
    $ export REGISTRY=docker.pkg.github.com
    ```

1.  Set the `IMAGE` environment variable to hold the image.

    ```
    $ export IMAGE=$REGISTRY/5gzorro/issm/issm-api:dfbbc7c
    ```

1.  Invoke the below command.

    ```
    $ docker build --tag "$IMAGE" --force-rm=true .
    ```

1.  Push the image.

    ```
    $ docker push "$IMAGE"
    ```
