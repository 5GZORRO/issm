# ISSM (Intelligent slice and service manager)

**Note: This is a work in progress. Ensure to monitor this repository frequently**

ISSM runs on kubernetes. You can use [these instructions](https://github.com/5GZORRO/infrastructure/blob/master/docs/kubernetes.md) to provision such a one

## Pre-requisites

* Ensure you have kafka broker already installed. You can use [these instructions](https://github.com/5GZORRO/infrastructure/blob/master/docs/kafka.md) to provision such a one
* Install argo and argo-events per [these instructions](docs/argo.md)
* Install vertical slicer per [these instructions](docs/slicer.md)
* Install datalake services: TBD
* Install discovery application per [these instructions](https://github.com/5GZORRO/Smart-Resource-and-Service-Discovery-application/blob/main/readme.txt)
* Install optimizer service per [these instructions](https://github.com/5GZORRO/issm-optimizer/blob/master/README.md)

## Deploy

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
                    value: 80
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

**Important:**
* the offers loaded into discovery application are of `VideoStreaming`, hence, ensure to [pre-onboard the corresponding blueprint](./scripts/slicer/onboard.md) into the vertical slicer.
* service owner (i.e mno/tenant) should be pre-defined along with SLA, hence ensure to [create it](./scripts/slicer/define_tenant.md) in the vertical slicer.
* service owner (i.e mno/tenant) should pre-exist in datalake, hence ensure to create it: TBD

As an alternative to the below, an [actuation script](scrips/actuator/README.md) can be used which automates most of the below steps

### Manual steps

**Important:**
* ensure to [create](https://github.com/5GZORRO/infrastructure/blob/master/docs/kafka.md#create-topics) `my-mno-topic` on ISSM kafka bus before publishing the intent

In a new terminal, log into ISSM Kafka container

Invoke the below command to publish an intent on ISSM topic providing a callback where progress and flow result are to be published.

```
/opt/kafka/bin/kafka-console-producer.sh --topic issm-topic --bootstrap-server localhost:9092
```

>{"event_uuid": "123", "operation": "submit_intent", "offered_price": "1700", "latitude": "56", "longitude": "5", "slice_segment": "edge", "category": "VideoStreaming", "qos_parameters": {"bandwidth": "30"}, "callback": {"type":"kafka", "kafka_topic": "my-mno-topic"}, "service_owner": "my-mno"}

The flow is invoked automatically

## Watch flow progress using Argo GUI

Browse to `http://<kubernetes master ipaddress>:2746`

## Consume flow progress (via callback)

In a new terminal, log into ISSM Kafka container

Consume latest updates reported on callback's topic

```
/opt/kafka/bin/kafka-console-consumer.sh --topic my-mno-topic --from-beginning --bootstrap-server localhost:9092
```
