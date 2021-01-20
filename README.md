# ISSM (Intelligent slice and service manager)

**Note: This is a work in progress. Ensure to monitor this repository frequently**

ISSM runs on kubernetes. You can use [these instructions](https://github.com/5GZORRO/infrastructure/blob/master/docs/kubernetes.md) to provision such a one

## Pre-requisite

* Ensure you have kafka broker already installed. You can use [these instructions](https://github.com/5GZORRO/infrastructure/blob/master/docs/kafka.md) to provision such a one
* Install argo and argo-events per [these instructions](docs/argo.md)
* Install discovery service per [these instructions](https://github.com/5GZORRO/smart-discovery-simulator/blob/master/README.md). Ensure to populate its data model with its `init.sh` script
* Install optimizer service per [these instructions](https://github.com/5GZORRO/issm-optimizer/blob/master/README.md)

## Deploy the service

Log into kuberneters master

Invoke the below in this order

```
kubectl create -n argo-events -f deploy/role.yaml
```

**Note:** you may need to update sensor's kafka and discovery services ips, ports according to your environment - before applying it on the system

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
```

```
envsubst < deploy/kafka-event-source.yaml.template | kubectl create -n argo-events -f -
```

```
kubectl apply -f deploy/issm-sensor.yaml -n argo-events
```

**Note:** Kafka `issm-topic` automatically get created during the onboarding of the event-source

## Deploy common template library

```
kubectl create -f wf-templates/base.yaml -n argo-events
```

## Trigger ISSM business flow

Log into your Kafka container

Invoke the below command to publish an intent on ISSM topic

```
 /opt/kafka/bin/kafka-console-producer.sh --topic issm-topic --bootstrap-server localhost:9092
```

>{"event_uuid": "123", "operation": "submit_intent", "location": "37.80 N, 23.75 E"}

The flow is invoked automatically

## Inspect result

Log into your Kafka container

Invoke the below command to obtain the latest message produced by the flow

```
/opt/kafka/bin/kafka-console-consumer.sh --topic service-owner --from-beginning --bootstrap-server localhost:9092
```

>{"data": {"event_uuid": "e50dfc010f62434fb3195e8feec86d74", "transaction_uuid": "123", "status": "success"}}
