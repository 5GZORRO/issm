#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

python3 ./cli.py --file ./free5gc-slice.yaml --service_owner operator-a --issm_api_url http://172.28.3.15:30080 --snfvo_name "free5gc slice snfvo" --product_offer_id  ff3635ff-7f9a-4475-8681-16248b610659
