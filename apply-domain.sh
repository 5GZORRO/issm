#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

ORCH=$1

echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Applying templates for domain: $MNO_NAMESPACE"
echo "Orchestrator type: $1"
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"


kubectl  delete  workflowtemplate --all -n  $MNO_NAMESPACE
kubectl  delete  sensor --all -n  $MNO_NAMESPACE

kubectl apply -f $SCRIPT_DIR/sensors/issm-domain-sensor-v2.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/sensors/issm-domain-sla-breach-sensor-v2.yaml -n $MNO_NAMESPACE

kubectl apply -f $SCRIPT_DIR/wf-templates/ -n $MNO_NAMESPACE

kubectl apply -f $SCRIPT_DIR/snfvo/ota.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/snfvo/spectrum.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/snfvo/vcdn.yaml -n $MNO_NAMESPACE

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
