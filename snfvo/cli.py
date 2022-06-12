#!/usr/bin/env python
import argparse
import requests
import yaml

'''
python3 ./cli.py --file ../../snfvo/ota.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name ota --product_offer_name "OTA demo eucnc core"
'''

def main():
    parser = argparse.ArgumentParser(description='A cli to load snfvo plugin into ISSM')
    parser.add_argument('--issm_api_url', help='URL to ISSM API service (e.g. http://172.28.3.15:30080)', required=True)
    parser.add_argument('--service_owner', help='The owner of this snfvo (e.g. operator-a)', required=True)
    parser.add_argument('--file', help='Path to snfvo yaml file (e.g. ./vcdn.yaml)', required=True)
    parser.add_argument('--snfvo_name', help='snfvo name (e.g. vcdn)', required=True)
    parser.add_argument('--product_offer_name', help='The name of the product offer this snfvo manages', required=True)

    args = parser.parse_args()

    try:
        f = open(args.file, 'r')
        _yaml = yaml.load(f, Loader=yaml.FullLoader)
    except:
        pass

    payload = {
        "snfvo_name": args.snfvo_name,
        "product_offer_name": args.product_offer_name,
        "snfvo_json": _yaml
    }

    headers = {'Content-Type': 'application/json'}
    r = requests.post(args.issm_api_url+'/snfvo/%s' % args.service_owner,
        json=payload,
        headers=headers)

if __name__ == '__main__':
    main()
