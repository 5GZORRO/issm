# ISSM

This is the __Intelligent slice and service manager__ component responsible for executing orchestration workflows in a context of a business transaction, such as extending a slice across a second domain in cooperation with the Network Slice and Service Orchestration.

## Pre-requisites

To install ISSM follow the installation guidelines per component following the below flow:
1. **Provision kubernetes cluster**. The guidelines are available [here](docs/kubernetes.md).
2. **Install kafka broker.** Follow the guidelines [here](docs/kafka.md).
3. **Install Datalake services**. Follow the guidelines [here](https://github.com/5GZORRO/datalake).
4. **Install SRSD**. Follow the guidelines [here](https://github.com/5GZORRO/Smart-Resource-and-Service-Discovery-application/tree/main/demo_June_21).
5. **Install ISSM-O**. Follow the guidelines [here](https://github.com/5GZORRO/issm-optimizer).

**Orchestration:**
For each mobile network operator (MNO), install either [NSSO](https://github.com/5GZORRO/nsso) or [ISSM-MEC-CNMP](https://github.com/5GZORRO/issm-mec-cnmp).

ISSM is comprised of a centralized component and a local instance running at the MNO premises

![Testbed](images/issm-distributed-0.5.png)


## Deploy ISSM centralized components

Log into 5GZorro platform kuberneters master

### Argo and Argo-events

Perform these [instructions](./docs/argo.md) to install Argo

### ISSM-API

Follow the guidelines [here](./api/README.md)

### Create Eventbus in issm namespace

```
kubectl create namespace issm
kubectl apply -n issm -f https://raw.githubusercontent.com/argoproj/argo-events/v1.1.0/examples/eventbus/native.yaml
```

### Create eventsource

Register an event source with platform communication fabric

Update kafka ip and port accordingly

```
export KAFKA_HOST=172.28.3.196
export KAFKA_PORT=9092
```

```
envsubst < deploy/kafka-sla-breach-event-source.yaml.template | kubectl apply -n issm -f -
```

### Add argo-event roles

Grant proper roles for issm sensor

```
kubectl apply -f deploy/install-v1.1.0.yaml
```

### Onboard SLA breach sensor

Create the sensor and templates

```
./apply-sla.sh
```

## Deploy ISSM local instance

Follow these instructions to install a local ISSM agent (sensor and flow templates) in the participating 5GZorro operators. Repeat this process for every operator (i.e. `operator-a`, `operator-b` and `operator-c`)

The below procedure applies to MNO (mobile network operator) `operator-a`

Log into `operator-a` kuberneters master

### Create MNO namespace

```
export MNO_NAME=operator-a
export MNO_NAMESPACE=domain-$MNO_NAME

kubectl create namespace $MNO_NAMESPACE
```

### Add Argo roles to MNO namespace

Run the below to add additional roles to `default` service account of the MNO namespace. These roles are used by the argo workflow controller

```
kubectl apply -f deploy/role.yaml -n $MNO_NAMESPACE
```

### Add Argo-event roles to MNO namespace

```
envsubst < deploy/install-v1.1.0-operator.yaml.template | kubectl apply -f -
```

### Add Eventbus to MNO namespace

```
kubectl apply -n $MNO_NAMESPACE -f https://raw.githubusercontent.com/argoproj/argo-events/v1.1.0/examples/eventbus/native.yaml
```

### Add kafka event source to MNO namespace

Register event source with platform communication fabric

Update kafka ip and port accordingly

```
export KAFKA_HOST=172.28.3.196
export KAFKA_PORT=9092

export ISSM_DOMAIN_TOPIC=issm-in-$MNO_NAME
envsubst < deploy/kafka-event-source.yaml.template | kubectl apply -n $MNO_NAMESPACE -f -

export SLA_BREACH_DOMAIN_TOPIC=issm-breach-$MNO_NAME
envsubst < deploy/kafka-domain-sla-breach-event-source.yaml.template | kubectl apply -n $MNO_NAMESPACE -f -
```

### Deploy sensor and templates

```
export MNO_NAME=operator-a
export MNO_NAMESPACE=domain-$MNO_NAME

./apply-domain.sh <ORCHESTRATOR>
```

`ORCHESTRATOR` denotes the orchestration being supported by the MNO

Valid values

* `NSSO` - refer to Network Slice and Service Orchestrator (see: https://github.com/5GZORRO/nsso/blob/main/README.md)
* `MEC` - refers to ISSM-MEC-CNMP (see: https://github.com/5GZORRO/issm-mec-cnmp/blob/master/README.md)
* `DUMMY` - simulator driver for testing ISSM

## Trigger ISSM business flow

Follow the guidelines [here](./api/README.md#api)

then watch business flow progress with Argo GUI (`http://<kubernetes master ipaddress>:2746`) running on the participated MNOs

## Licensing

This 5GZORRO component is published under Apache 2.0 license. Please see the [LICENSE](./LICENSE) file for further details.