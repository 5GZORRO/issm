#!/bin/bash

export MDA_URL="172.28.3.42:32732"
curl -d @spec_latest.json -X POST http://$MDA_URL/settings --header "Content-Type:application/json"

