#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


kubectl apply -f $SCRIPT_DIR/flows/issm-sla-breach-sensor-v2.yaml -n issm

kubectl delete workflowtemplates --all -n issm

kubectl apply -f $SCRIPT_DIR/wf-templates/base.yaml -n issm
kubectl apply -f $SCRIPT_DIR/wf-templates/breach-v2.yaml -n issm
kubectl apply -f $SCRIPT_DIR/wf-templates/transaction-v2.yaml -n issm
kubectl apply -f $SCRIPT_DIR/wf-templates/environment-v2.yaml -n issm
