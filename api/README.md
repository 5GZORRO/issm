# issm-api

ISSM-API provides management API endpoints for create, delete and list transactions.

## Pre-requisites

issm-api calls into argo-server REST endpoints.

* Argo server is automatically installed with argo and is internally available within kubernetes
* Expose argo-server externally via these [instructions](https://argoproj.github.io/argo-workflows/argo-server/#expose-a-loadbalancer): `kubectl patch svc argo-server -n argo -p '{"spec": {"type": "LoadBalancer"}}'`

## Deploy the service

Log into kuberneters master

Invoke the below in this order

**Note:** you may need to update below settings according to your environment

```
export REGISTRY=docker.pkg.github.com
export IMAGE=$REGISTRY/5gzorro/issm/issm-api:8cff61e

export ISSM_KAFKA_HOST=172.28.3.196
export ISSM_KAFKA_PORT=9092

# cluster-IP
export ARGO_SERVER=10.43.79.33:2746

# externally accessed argo-server
export LB_ARGO_SERVER=172.28.3.15:30753
```

Deploy

```
kubectl apply -f deploy/role.yaml -n issm
envsubst < deploy/deployment.yaml.template | kubectl apply -n issm -f -
kubectl apply -f deploy/service.yaml -n issm
```

## API (transaction)

### Get transaction types

Returns a list of supported transaction types

```
curl -H "Content-type: application/json" -X GET http://issm_api_ip_address:30080/transactions_types
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
```

Return:

```
    status - 200
    list of transaction types (list of str)
```

Invocation example:

```
    curl -H "Content-type: application/json" -X GET http://172.28.3.15:30080/transactions_types
    [
      "instantiate",
      "scaleout"
    ]
```

### Submit transaction

Submit a transaction for the given service owner

```
curl -H "Content-type: application/json" -X POST -d "@/path/to/intent/json" http://issm_api_ip_address:30080/transactions/<service_owner>/<transaction_type>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner       - the service owner (str)
    transaction_type    - the type of the transaction to submit (e.g. instantiate, scaleout)
```

Data intent:

refer [here](intents/README.md) for more information

Return:

```
    status - 200
    transaction_uuid - the transaction uuid of this business flow instance (uuid)
```

Invocation example:

```
    curl -H "Content-type: application/json" -X POST -d "@intents/vcdn/intent-instantiate.json" http://172.28.3.15:30080/transactions/operator-a/instantiate

    {
        "transaction_uuid": "cc0bb0e0fe214705a9222b4582f17961"
    }
```

### List transactions

Returns all transactions of the service owner

```
curl -H "Content-type: application/json" -X GET http://issm_api_ip_address:30080/transactions/<service_owner>
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
    curl -H "Content-type: application/json" -X GET http://172.28.3.15:30080/transactions/operator-a
[
  {
    "ref": "http://172.28.3.15:32026/workflows/domain-operator-a?label=transaction_uuid=b81c8c6cade04317b8c9240bb137715a",
    "created": "2022-01-19T12:28:42+00:00",
    "status": "Failed",
    "transaction_type": "scaleout",
    "transaction_uuid": "b81c8c6cade04317b8c9240bb137715a"
  },
  {
    "ref": "http://172.28.3.15:32026/workflows/domain-operator-a?label=transaction_uuid=86804b8548ff4bd8a914c12ef862a993",
    "created": "2022-01-17T17:28:01+00:00",
    "status": "Succeeded",
    "transaction_type": "instantiate",
    "transaction_uuid": "86804b8548ff4bd8a914c12ef862a993"
  },
  {
    "ref": "http://172.28.3.15:32026/workflows/domain-operator-a?label=transaction_uuid=9e20c8d3cf5d4a448810af4f9cc318a8",
    "created": "2021-12-15T10:58:59+00:00",
    "status": "Succeeded",
    "transaction_type": "scaleout",
    "transaction_uuid": "9e20c8d3cf5d4a448810af4f9cc318a8"
  }
]
```

### List transactions from a given type

Returns transactions of a given type of the service owner

```
curl -H "Content-type: application/json" -X GET http://issm_api_ip_address:30080/transactions/<service_owner>/<transaction_type>
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
    curl -H "Content-type: application/json" -X GET http://172.28.3.15:30080/transactions/operator-a/scaleout
    [
      {
        "ref": "http://172.28.3.15:32026/workflows/domain-operator-a?label=transaction_uuid=c5df607af95f469ca058919989968a33",
        "created": "2022-01-19T12:28:42+00:00",
        "status": "Running",
        "transaction_type": "scaleout",
        "transaction_uuid": "c5df607af95f469ca058919989968a33"
      },
      {
        "ref": "http://172.28.3.15:32026/workflows/domain-operator-a?label=transaction_uuid=6261754de98c4537ba08bd6b3c8d7d36",
        "created": "2022-01-19T12:40:42+00:00",
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

## API (snfvo)


### Create snfvo

Create snfvo with the given name, the product offer it manages, and the management flow logic defined as an Argo WorkflowTemplate CR

```
curl -H "Content-type: application/json" -X POST -d '{"product_offer_id": "<string>", "snfvo_name": "<string>", "snfvo_json": "<json>"}' http://issm_api_ip_address:30080/snfvo/<service_owner>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner       - the service owner (str)
```

Data payload:

```
    snfvo_name       - the name of the snfvo (str - free text)
    product_offer_id - the id of the product offer for this snfvo (str - uuid)
    snfvo_json       - the snfvo WorkflowTemplate CR that defines the management logic flow (WorkflowTemplate json)
```

Return:

```
    status - 200
```

Invocation example:

A sample python cli had been implemented to simplify the creation of an snfvo. Refer [here](../snfvo/cli.py) for more details


### List snfvo

Returns all snfvos of the service owner

```
curl -H "Content-type: application/json" -X GET http://issm_api_ip_address:30080/snfvo/<service_owner>
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
        snfvo_name - the name of the snvfo (str - free text)
        product_offer_id - the id of the product offer for this snfvo (str - uuid)
```

Invocation example:

```
    curl -H "Content-type: application/json" -X GET  http://172.28.3.15:30080/snfvo/operator-a
[
  {
    "snfvo_name": "OTA demo eucnc core",
    "product_offer_id": "642d5460-53c1-4f97-9a50-702238f70ac6"
  },
  {
    "snfvo_name": "Slice Offer UC2",
    "product_offer_id": "2ed69036-81ba-4e9a-a194-c066cea20847"
  },
  {
    "snfvo_name": "CDN Network Service (CDN+SAS)",
    "product_offer_id": "72ce9b8b-532a-4064-a364-181fb4f5013e"
  }
]
```

### Delete snfvo

Delete snfvo with the given name, and owner

```
curl -H "Content-type: application/json" -X DELETE http://issm_api_ip_address:30080/snfvo/<service_owner>/<product_offer_id>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner       - the service owner (str)
    product_offer_id    - the id of the product offer for this snfvo (str)
```

Return:

```
    status - 200
```

Invocation example:

```
 curl -H "Content-type: application/json" -X DELETE http://172.28.3.15:30080/snfvo/operator-c/2ed69036-81ba-4e9a-a194-c066cea20847
```

## Build (**relevant for developers only**)

1.  Set the `REGISTRY` environment variable to hold the name of your docker registry. The following command sets it
    equal to the docker github package repository.

    ```
    $ export REGISTRY=docker.pkg.github.com
    ```

1.  Set the `IMAGE` environment variable to hold the image.

    ```
    $ export IMAGE=$REGISTRY/5gzorro/issm/issm-api:8cff61e
    ```

1.  Invoke the below command.

    ```
    $ docker build --tag "$IMAGE" --force-rm=true .
    ```

1.  Push the image.

    ```
    $ docker push "$IMAGE"
    ```
