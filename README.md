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

### Create operator namespaces

Orchestration workflows will invoked locally in the operator namespace

operator-a

```
kubectl create namespace domain-operator-a
```

and operator-b

```
kubectl create namespace domain-operator-b
```

### Add roles to operator namespaces

Run the below to add additional roles to `default` service account of the operator namespace. These roles are used by argo workflow

operator-a

```
kubectl create -f deploy/role.yaml -n domain-operator-a
```

and operator-b

```
kubectl create -f deploy/role.yaml -n domain-operator-b
```

### Add argo-event roles to operator namespaces

operator-a

```
kubectl apply -f deploy/install-v1.1.0-operator-a.yaml
```

and operator-b

```
kubectl apply -f deploy/install-v1.1.0-operator-b.yaml
```

### Create Eventbus in operator namespaces

operator-a

```
kubectl apply -n domain-operator-a -f https://raw.githubusercontent.com/argoproj/argo-events/v1.1.0/examples/eventbus/native.yaml
```
and operator-b

```
kubectl apply -n domain-operator-b -f https://raw.githubusercontent.com/argoproj/argo-events/v1.1.0/examples/eventbus/native.yaml
```

### Create kafka event sources for ISSM bus

Update ISSM kafka ip and port settings per your environment

```
export KAFKA_HOST=172.28.3.196
export KAFKA_PORT=9092
```

create the sources

```
envsubst < deploy/kafka-sla-breach-event-source.yaml.template | kubectl create -n issm -f -
```

operator-a

```
export ISSM_DOMAIN_TOPIC=issm-domain-operator-a
envsubst < deploy/kafka-event-source.yaml.template | kubectl create -n domain-operator-a -f -
```

and operator-b

```
export ISSM_DOMAIN_TOPIC=issm-domain-operator-b
envsubst < deploy/kafka-event-source.yaml.template | kubectl create -n domain-operator-b -f -
```

**Note:** Kafka topics are automatically created during the creation of the event sources

### Apply docker-secrete.yaml

Create docker-secrete.yaml file per [these instructions](docs/kubernetes-private-dockerregistry.md) and apply it. This secrete is for ISSM orchestrator to pull images from docker.pkg.github.com

```
kubectl apply -f docker-secrete.yaml -n issm
kubectl apply -f docker-secrete.yaml -n domain-operator-a
kubectl apply -f docker-secrete.yaml -n domain-operator-b
```

### Onboard SLA breach workflow

```
kubectl apply -f flows/issm-sla-breach-sensor.yaml -n issm
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
```

then, onboard the flow

operator-a

```
kubectl apply -f flows/issm-sensor.yaml -n domain-operator-a
```

and operator-b

```
kubectl apply -f flows/issm-sensor.yaml -n domain-operator-b
```

### Deploy common templates

Deploy common utilities and NSSO libraries

operator-a

```
kubectl apply -f wf-templates/intent.yaml -n domain-operator-a
kubectl apply -f wf-templates/orchestration.yaml -n domain-operator-a
kubectl apply -f wf-templates/base.yaml -n domain-operator-a
kubectl apply -f wf-templates/slice.yaml -n domain-operator-a
```

and operator-b

```
kubectl apply -f wf-templates/intent.yaml -n domain-operator-b
kubectl apply -f wf-templates/orchestration.yaml -n domain-operator-b
kubectl apply -f wf-templates/base.yaml -n domain-operator-b
kubectl apply -f wf-templates/slice.yaml -n domain-operator-b
```

## Trigger ISSM business flow

Follow the guidelines [here](https://github.com/5GZORRO/issm/tree/master/api#api)

then watch business flow progress with Argo GUI (`http://<kubernetes master ipaddress>:2746`)

## Licensing

This 5GZORRO component is published under Apache 2.0 license. Please see the [LICENSE](./LICENSE) file for further details.