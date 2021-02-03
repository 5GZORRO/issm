# ISSM (Intelligent slice and service manager)

**Note: This is a work in progress. Ensure to monitor this repository frequently**

ISSM runs on kubernetes. You can use [these instructions](https://github.com/5GZORRO/infrastructure/blob/master/docs/kubernetes.md) to provision such a one

## Pre-requisite

* Ensure you have kafka broker already installed. You can use [these instructions](https://github.com/5GZORRO/infrastructure/blob/master/docs/kafka.md) to provision such a one
* Install argo and argo-events per [these instructions](docs/argo.md)
* Install discovery service per [these instructions](https://github.com/5GZORRO/smart-discovery-simulator/blob/master/README.md). Ensure to populate its data model with its `init.sh` script
* Install optimizer service per [these instructions](https://github.com/5GZORRO/issm-optimizer/blob/master/README.md)
* Install vertical slicer per [these instructions](docs/slicer.md)

## Deploy the service

Deploying the service comprises these two steps:

* Set ISSM role
* Create ISSM kafka sink

Log into kuberneters master

Invoke the below in this order

### Set ISSM role

```
kubectl create -n argo-events -f deploy/role.yaml
```

### Create ISSM kafka event source

Update ISSM kafka bus ip and port

```
export KAFKA_HOST=10.20.3.4
export KAFKA_PORT=9092
```

```
envsubst < deploy/kafka-event-source.yaml.template | kubectl create -n argo-events -f -
```

**Note:** Kafka `issm-topic` is automatically created during the creation of the event-source

### Create ISSM optimizer topic

Follow [create-topics](https://github.com/5GZORRO/infrastructure/blob/master/docs/kafka.md#create-topics) to create `issm-optmizer` topic

## Onboard ISSM flow

Depending on the flow context, you may need to customize it with access information to the 5G Zorro services the flow depends on

Open `flows/issm-sensor.yaml`

Update access info for:

* ISSM kafka bus with the values set [above](./README.md#create-issm-kafka-event-source)
* Discovery service
* Vertical slicer service

```
                arguments:
                  parameters:
                  - name: kafka_ip
                    value: 10.20.3.4
                  - name: kafka_port
                    value: 9092
                  - name: discovery_service_ip
                    value: 10.20.4.2
                  - name: discovery_service_port
                    value: 31848
                  - name: slicer_ip
                    value: 1.2.3.4

```

Onboard the flow

```
kubectl apply -f flows/issm-sensor.yaml -n argo-events
```

## Deploy common template library

```
kubectl create -f wf-templates/base.yaml -n argo-events
kubectl create -f wf-templates/slice.yaml -n argo-events
```

## Trigger ISSM business flow

In a new terminal, log into ISSM Kafka container

Invoke the below command to publish an intent on ISSM topic providing a callback where progress and flow result are to be published.

**Note:** for kafka callback ISSM kafka bus is being used

```
/opt/kafka/bin/kafka-console-producer.sh --topic issm-topic --bootstrap-server localhost:9092
```

>{"event_uuid": "123", "operation": "submit_intent", "location": "37.80 N, 23.75 E", "callback": {"type": "kafka", "kafka_topic": "my-mno-topic"}, "mno_name": "my-mno"}

The flow is invoked automatically

## Inspect result

In a new terminal, log into ISSM Kafka container

Invoke the below command to obtain the latest message produced by the flow

```
/opt/kafka/bin/kafka-console-consumer.sh --topic my-mno-topic --from-beginning --bootstrap-server localhost:9092
```

>{"data": {"event_uuid": "e50dfc010f62434fb3195e8feec86d74", "transaction_uuid": "123", "status": "success"}}
