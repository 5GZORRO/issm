#!/bin/bash

export MDA_URL="172.28.3.42:32732"
curl -X DELETE http://$MDA_URL/settings/$1

