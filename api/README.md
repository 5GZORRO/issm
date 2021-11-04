# issm-api

Component responsible for providing management API endpoint service for ISSM.

## Deploy the service

Log into 5GZorro platform kuberneters master (where ISSM platform is installed)

Invoke the below in this order

**Note:** you may need to update below settings according to your environment

```
export REGISTRY=docker.pkg.github.com
export IMAGE=$REGISTRY/5gzorro/issm/issm-api:temp

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

### List workflows

Returns the workflows invoked by the service owner

```
curl -H "Content-type: application/json" -GET http://issm_api_ip_address:30080/get_workflows/<service_owner>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner       - the id of the service owner/tenant that triggered the workflows (str)
```

Return:

```
    status - 200
    items - list of returned workflows (json)
```


Invocation example:

```
    curl -H "Content-type: application/json" -GET http://172.28.3.42:30080/get_workflows/operator-a

    {
      "items": [
        {
          "metadata": {
            "creationTimestamp": "2021-11-04T09:16:55Z",
            "labels": {
              "transaction_uuid": "98c97e113ed64d538c27c63a0c8fb152"
            },
            "name": "580be51686b144a6a468a97f8e3651a5"
          },
          "status": {
            "phase": "Succeeded"
          }
        },
        {
          "metadata": {
            "creationTimestamp": "2021-11-04T09:16:40Z",
            "labels": {
              "transaction_uuid": "98c97e113ed64d538c27c63a0c8fb152"
            },
            "name": "98c97e113ed64d538c27c63a0c8fb152"
          },
          "status": {
            "phase": "Succeeded"
          }
        }
      ]
    }
```


### Get workflow reference

Returns a GUI URL for showing a transaction invoked by the service owner

```
curl -H "Content-type: application/json" -GET http://issm_api_ip_address:30080/get_workflow_ref/<service_owner>/<transaction_uuid>
```

REST path:

```
    issm_api_ip_address - ipaddress ISSM API service.
    service_owner       - the id of the service owner that triggered the workflows (str)
    transaction_uuid    - the transaction uuid of this business flow instance (uuid)
```

Return:

```
    status - 200
    items - list of returned workflows (json)
```

Invocation example:

```
    curl -H "Content-type: application/json" -GET http://172.28.3.42:30080/get_workflow_ref/operator-a/98c97e113ed64d538c27c63a0c8fb152

    {
      "ref": "http://172.28.3.42:32026/workflows/domain-operator-a?label=transaction_uuid=98c97e113ed64d538c27c63a0c8fb152"
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
