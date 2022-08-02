#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

ORCH=$1

echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Applying templates for domain: $MNO_NAME"
echo "Orchestrator type: $1"
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

MNO_NAMESPACE=domain-$MNO_NAME

kubectl  delete  es --all -n  $MNO_NAMESPACE
kubectl  delete  workflowtemplate --all -n  $MNO_NAMESPACE
kubectl  delete  sensor --all -n  $MNO_NAMESPACE

KAFKA_HOST=172.28.3.196
KAFKA_PORT=9092

ISSM_DOMAIN_TOPIC=issm-in-$MNO_NAME
envsubst < $SCRIPT_DIR/deploy/kafka-event-source.yaml.template | kubectl apply -n $MNO_NAMESPACE -f -

SLA_BREACH_DOMAIN_TOPIC=issm-breach-$MNO_NAME
envsubst < $SCRIPT_DIR/deploy/kafka-domain-sla-breach-event-source.yaml.template | kubectl apply -n $MNO_NAMESPACE -f -

AUX_DOMAIN_TOPIC=issm-aux-$MNO_NAME
envsubst < $SCRIPT_DIR/deploy/kafka-domain-aux-event-source.yaml.template | kubectl apply -n $MNO_NAMESPACE -f -

kubectl apply -f $SCRIPT_DIR/sensors/issm-domain-sensor-v2.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/sensors/issm-domain-sla-breach-sensor-v2.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/sensors/issm-domain-aux-sensor-v2.yaml -n $MNO_NAMESPACE

kubectl apply -f $SCRIPT_DIR/wf-templates/ -n $MNO_NAMESPACE

if [ "$ORCH" = "NSSO" ]; then
    kubectl apply -f $SCRIPT_DIR/wf-orchestrators/orchestration-nsso-v2.yaml -n $MNO_NAMESPACE
elif [ "$ORCH" = "MEC" ]; then
    kubectl apply -f $SCRIPT_DIR/wf-orchestrators/orchestration-mec-cnmp-v2.yaml -n $MNO_NAMESPACE
elif [ "$ORCH" = "DUMMY" ]; then
    kubectl apply -f $SCRIPT_DIR/wf-orchestrators/orchestration-dummy-v2.yaml -n $MNO_NAMESPACE
else
    echo "Illegal Orchestrator type value: [$1]"
    exit 1
fi
