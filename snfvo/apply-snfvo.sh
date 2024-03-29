#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

python3 ./cli.py --file ./free5gc-slice.yaml --service_owner operator-a --issm_api_url http://172.28.3.15:30080 --snfvo_name "free5gc slice snfvo" --product_offer_id  ff3635ff-7f9a-4475-8681-16248b610659

python3 ./cli.py --file ./free5gc-core.yaml --service_owner operator-a --issm_api_url http://172.28.3.15:30080 --snfvo_name "free5gc core snfvo" --product_offer_id  86a8a9bc-5709-4096-98ba-65321c7d9825

python3 ./cli.py --file ./vcache.yaml --service_owner operator-a --issm_api_url http://172.28.3.15:30080 --snfvo_name "vcache container snfvo" --product_offer_id  2b50ac88-98c7-4894-a4b1-ad9b6ac5c3e7

python3 ./cli.py --file ./vcdn-on-slice.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "vcache on slice snfvo" --product_offer_id  df5cd8c8-2617-45f8-9f21-def40cda6dc1

python3 ./cli.py --file ./vcdn.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "CDN service" --product_offer_id  73c10922-7927-4792-ad5f-033471d826ed
