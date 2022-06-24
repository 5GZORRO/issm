#!/usr/bin/env python
import argparse
import requests
import yaml

'''
python3 ./cli.py --file ./vcdn.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "CDN Network Service (CDN+SAS)" --product_offer_id 28538e5b-5902-4f59-898d-e6fc3bf12e3a

python3 ./cli.py --file ./ota.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "OTA demo eucnc core" --product_offer_id d570d2a2-02e7-465b-9d24-ee073fd077af

python3 ./cli.py --file ./spectrum.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name "Slice Offer UC2" --product_offer_id 91a0a81d-5434-47be-a1a1-c724babc2e50
'''

def main():
    parser = argparse.ArgumentParser(description='A cli to load snfvo plugin into ISSM')
    parser.add_argument('--issm_api_url', help='URL to ISSM API service (e.g. http://172.28.3.15:30080)', required=True)
    parser.add_argument('--service_owner', help='The owner of this snfvo (e.g. operator-c)', required=True)
    parser.add_argument('--file', help='Path to snfvo yaml file (e.g. ./ota.yaml)', required=True)
    parser.add_argument('--snfvo_name', help='snfvo name (e.g. OTA demo eucnc core)', required=True)
    parser.add_argument('--product_offer_id', help='The id of the product offer this snfvo manages', required=True)

    args = parser.parse_args()

    try:
        f = open(args.file, 'r')
        _yaml = yaml.load(f, Loader=yaml.FullLoader)
    except:
        pass

    payload = {
        "snfvo_name": args.snfvo_name,
        "product_offer_id": args.product_offer_id,
        "snfvo_json": _yaml
    }

    headers = {'Content-Type': 'application/json'}
    r = requests.post(args.issm_api_url+'/snfvo/%s' % args.service_owner,
        json=payload,
        headers=headers)
    r.raise_for_status()

if __name__ == '__main__':
    main()
