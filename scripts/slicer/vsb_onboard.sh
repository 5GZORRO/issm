#!/bin/bash

#
# Helper script to onboared a given blueprint.
#

export SLICER="localhost"
export BETWEEN=3

echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Login admin.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -i -X POST -d username=admin -d password=admin -c ./admin_credentials http://$SLICER:8082/login 2>/dev/null

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Create blueprint"
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b ./admin_credentials -d @vsb_VideoStreaming.json -X POST http://$SLICER:8082/portal/catalogue/vsblueprint --header "Content-Type:application/json"
