#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

ORCH=$1

kubectl apply -f $SCRIPT_DIR/flows/issm-sensor.yaml -n $MNO_NAMESPACE

kubectl apply -f $SCRIPT_DIR/wf-templates/base.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/scenarios/1/scenario-1-submit.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/scenarios/2/scenario-2-submit.yaml -n $MNO_NAMESPACE

if [ "$ORCH" = "NSSO" ]; then
    kubectl apply -f $SCRIPT_DIR/scenarios/1/orch-nsso.yaml -n $MNO_NAMESPACE
    kubectl apply -f $SCRIPT_DIR/scenarios/2/orch-nsso.yaml -n $MNO_NAMESPACE
else
    kubectl apply -f $SCRIPT_DIR/scenarios/1/orch-mec-cnmp.yaml -n $MNO_NAMESPACE
    kubectl apply -f $SCRIPT_DIR/scenarios/2/orch-mec-cnmp.yaml -n $MNO_NAMESPACE
fi