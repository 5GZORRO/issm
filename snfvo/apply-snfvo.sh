#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

python3 ./cli.py --file ./ota-composite.yaml --service_owner operator-e --issm_api_url http://10.4.2.126:30080 --snfvo_name "OTA Composite Offer" --product_offer_id  2d9951f5-aa8e-4d0a-a91a-5b23b5cea0e4
