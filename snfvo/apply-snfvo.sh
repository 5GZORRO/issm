#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# snfvo to get onboarded into operator-c that purchased core offer
python3 ./cli.py --file ./ota.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "OTA demo eucnc core" --product_offer_id d570d2a2-02e7-465b-9d24-ee073fd077af

python3 ./cli.py --file ./spectrum.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "Slice Offer UC2" --product_offer_id 91a0a81d-5434-47be-a1a1-c724babc2e50
python3 ./cli.py --file ./spectrum-slice.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "Slice offer with configurable spectrum" --product_offer_id 00abbe8a-839d-4999-b9aa-aeda91850c23

python3 ./cli.py --file ./vcdn.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "CDN Network Service (CDN+SAS)" --product_offer_id ea383187-ffba-49a5-a465-7276820a509c
python3 ./cli.py --file ./vcdn-mec-cnmp.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "vCDN Optimized Service (e2e test of ISSM-O)" --product_offer_id 416767e2-cd33-4b62-b2d5-074aaa156004

# snfvo to get onboarded into operator-b that purchased the composite offer
python3 ./cli.py --file ./ota-composite.yaml --service_owner operator-b --issm_api_url http://172.28.3.15:30080 --snfvo_name "OTA Composite Offer" --product_offer_id a4de0666-2820-4666-8186-d193d8b44e25
