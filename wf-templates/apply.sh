#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

ORCH=$1

kubectl apply -f $SCRIPT_DIR/base.yaml -n $MNO_NAMESPACE
kubectl apply -f $SCRIPT_DIR/submit.yaml -n $MNO_NAMESPACE

if [ "$ORCH" = "NSSO" ]; then
    kubectl apply -f $SCRIPT_DIR/slice.yaml -n $MNO_NAMESPACE
    kubectl apply -f $SCRIPT_DIR/orchestration.yaml -n $MNO_NAMESPACE
else
    kubectl apply -f $SCRIPT_DIR/orchestration-mec-cnmp.yaml -n $MNO_NAMESPACE
fi