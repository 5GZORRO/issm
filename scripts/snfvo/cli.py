#!/usr/bin/env python
import argparse
import requests
import yaml

'''
python3 ./cli.py --file ../../snfvo/ota.yaml --service_owner operator-c --issm_api_url http://172.28.3.15:30080 --snfvo_name ota --snfvo_criteria "OTA demo eucnc core"
'''

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--service_owner', help='')
    parser.add_argument('--issm_api_url', help='')
    parser.add_argument('--file', help='')
    parser.add_argument('--snfvo_name', help='')
    parser.add_argument('--snfvo_criteria', help='')

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
