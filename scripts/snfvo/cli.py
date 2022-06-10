#!/usr/bin/env python
import argparse
import requests
import yaml

'''
python3 ./cli.py --file ../../snfvo/ota.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name ota --snfvo_criteria "OTA demo eucnc core"
'''

def main():
    parser = argparse.ArgumentParser(description='A cli to load snfvo plugin into ISSM')
    parser.add_argument('--issm_api_url', help='URL to ISSM API service (e.g. http://172.28.3.15:30080)')
    parser.add_argument('--service_owner', help='The owner of this snfvo (e.g. operator-a)')
    parser.add_argument('--file', help='Path to snfvo yaml file (e.g. ./vcdn.yaml)')
    parser.add_argument('--snfvo_name', help='snfvo name (e.g. vcdn)')
    # TODO: consider renaming snfvo_criteria to product_offer_name
    parser.add_argument('--snfvo_criteria', help='Runtime definition to load this snfvo')

    args = parser.parse_args()

    try:
        f = open(args.file, 'r')
        _yaml = yaml.load(f, Loader=yaml.FullLoader)
    except:
        pass

    payload = {
        "snfvo_name": args.snfvo_name,
        "criteria_name": args.snfvo_criteria,
        "snfvo_json": _yaml
    }

    headers = {'Content-Type': 'application/json'}
    r = requests.post(args.issm_api_url+'/snfvo/%s' % args.service_owner,
        json=payload,
        headers=headers)

if __name__ == '__main__':
    main()
