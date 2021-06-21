#!/bin/bash

#
# Helper script to onboared a given blueprint.
#

export BETWEEN=3

echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Login admin.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -i -X POST -d username=admin -d password=admin -c ./admin_credentials http://$SLICER_URL/login 2>/dev/null

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Delete VSIs"
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b ./admin_credentials -X PUT -d '{"nsiId": "42"}' http://$SLICER_URL/vs/basic/nslcm/ns/42/action/terminate --header "Content-Type:application/json"