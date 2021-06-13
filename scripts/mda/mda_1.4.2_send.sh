#!/bin/bash

export MDA_URL="172.28.3.42:31859"
curl -d @spec_1.4.2.json -X POST http://$MDA_URL/settings --header "Content-Type:application/json"
