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

kubectl apply -f $SCRIPT_DIR/flows/issm-sensor.yaml -n $MNO_NAMESPACE

kubectl apply -f $SCRIPT_DIR/wf-templates/base.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/scenarios/1/scenario-1-submit.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/scenarios/uc3/uc3-submit.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/scenarios/uc1.2/uc1.2-submit.yaml -n $MNO_NAMESPACE

if [ "$ORCH" = "NSSO" ]; then
    kubectl apply -f $SCRIPT_DIR/scenarios/1/orch-nsso.yaml -n $MNO_NAMESPACE
    kubectl apply -f $SCRIPT_DIR/scenarios/uc1.2/orch-nsso.yaml -n $MNO_NAMESPACE
    kubectl apply -f $SCRIPT_DIR/scenarios/uc3/orch-nsso.yaml -n $MNO_NAMESPACE
elif [ "$ORCH" = "MEC" ]; then
    kubectl apply -f $SCRIPT_DIR/scenarios/1/orch-mec-cnmp.yaml -n $MNO_NAMESPACE
    kubectl apply -f $SCRIPT_DIR/scenarios/uc1.2/orch-mec-cnmp.yaml -n $MNO_NAMESPACE
    kubectl apply -f $SCRIPT_DIR/scenarios/uc3/orch-mec-cnmp.yaml -n $MNO_NAMESPACE
else
    echo "Illegal Orchestrator type value: [$1]"
    exit 1
fi
