#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


kubectl apply -f $SCRIPT_DIR/flows/issm-sla-breach-sensor.yaml -n issm

kubectl apply -f $SCRIPT_DIR/wf-templates/base.yaml -n issm
kubectl apply -f $SCRIPT_DIR/scenarios/1/scenario-1-breach.yaml -n issm
kubectl apply -f $SCRIPT_DIR/scenarios/2/scenario-2-breach.yaml -n issm
