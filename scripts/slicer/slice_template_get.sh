#!/bin/bash

#
# Helper script to onboared a given blueprint.
#

export BETWEEN=3

echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Login operator-a.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -i -X POST -d username=admin -d password=admin -c ./admin_credentials http://$SLICER_URL/login 2>/dev/null

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "List slice templates"
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b ./admin_credentials -X GET http://$SLICER_URL/ns/catalogue/nstemplate --header "Content-Type:application/json" | jq .