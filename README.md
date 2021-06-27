# ISSM

This is the __Intelligent slice and service manager__ component responsible for executing orchestration workflows in a context of a business transaction, such as extending a slice across a second domain in cooperation with the Network Slice and Service Orchestration.

## Pre-requisites

To install ISSM follow the installation guidelines per component following the below flow:
1. **Provision kubernetes cluster**. The guidelines are available [here](docs/kubernetes.md).
2. **Install kafka broker.** Follow the guidelines [here](docs/kafka.md).
3. **Install Argo and Argo-events**. Follow the guidelines [here](docs/argo.md).
4. **Install Datalake services**. Follow the guidelines [here](https://github.com/5GZORRO/datalake).
5. **Install NSSO**. Follow the guidelines [here](https://github.com/5GZORRO/nsso).
6. **Install SRSD**. Follow the guidelines [here](https://github.com/5GZORRO/Smart-Resource-and-Service-Discovery-application/tree/main/demo_June_21).
7. **Install ISSM-API**. Follow the guidelines [here](api).
8. **Install ISSM-O**. Follow the guidelines [here](https://github.com/5GZORRO/issm-optimizer).

## Deploy

Log into kuberneters master and perform the below in this order

### Set ISSM role

```
kubectl create -n argo-events -f deploy/role.yaml
```

### Create ISSM kafka event sources

Update ISSM kafka ip and port settings per your environment

```
export KAFKA_HOST=172.28.3.196
export KAFKA_PORT=9092
```

create the sources

```
envsubst < deploy/kafka-event-source.yaml.template | kubectl create -n argo-events -f -
envsubst < deploy/kafka-sla-breach-event-source.yaml.template | kubectl create -n argo-events -f -
```

**Note:** Kafka `issm-topic` , `isbp-topic-out` are automatically created during the creation of the event sources

### Apply docker-secrete.yaml

Create docker-secrete.yaml file per [these instructions](docs/kubernetes-private-dockerregistry.md) and apply it. This secrete is for ISSM orchestrator to pull images from docker.pkg.github.com

```
kubectl apply -f docker-secrete.yaml -n argo-events
```

### Onboard SLA breach workflow

```
kubectl apply -f flows/issm-sla-breach-sensor.yaml -n argo-events
```

### Onboard orchestration workflow

First, customize the workflow with access information to the 5G Zorro services

Open `flows/issm-sensor.yaml`

Update access info for:

* ISSM kafka bus
* Datalake kafka bus
* Smart resource and service discovery
* Network slice and service orchestration

```
                arguments:
                  parameters:
                  - name: kafka_ip
                    value: 172.28.3.196
                  - name: kafka_port
                    value: 9092
                  - name: kafka_dl_ip
                    value: 172.28.3.196
                  - name: kafka_dl_port
                    value: 9092
                  - name: discovery_ip
                    value: 172.28.3.42
                  - name: discovery_port
                    value: 32000
                  - name: nsso_ip
                    value: 172.28.3.42
                  - name: nsso_port
                    value: 31082
```

then, onboard the flow

```
kubectl apply -f flows/issm-sensor.yaml -n argo-events
```

### Deploy common templates

Deploy common utilities and NSSO libraries

```
kubectl create -f wf-templates/base.yaml -n argo-events
kubectl create -f wf-templates/slice.yaml -n argo-events
```

## Trigger ISSM business flow

Follow the guidelines [here](https://github.com/5GZORRO/issm/tree/master/api#api)

then watch business flow progress with Argo GUI (`http://<kubernetes master ipaddress>:2746`)

## Licensing

This 5GZORRO component is published under Apache 2.0 license. Please see the [LICENSE](./LICENSE) file for further details.