#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

python3 ./cli.py --file ./opt-topology.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "OTA Composite Offer" --product_offer_id  673db4c4-c2a4-4348-9e54-0f916f56d5d9
