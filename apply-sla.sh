#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


kubectl delete workflowtemplates --all -n issm
kubectl  delete  sensor --all -n  issm

kubectl apply -f $SCRIPT_DIR/flows/issm-sla-breach-sensor-v2.yaml -n issm

kubectl apply -f $SCRIPT_DIR/wf-templates/base.yaml -n issm
