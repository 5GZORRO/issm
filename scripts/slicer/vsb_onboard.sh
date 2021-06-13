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
echo "Create blueprint"
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b ./admin_credentials -d @vsb_vCDN_edge_ICOM.json -X POST http://$SLICER_URL/portal/catalogue/vsblueprint --header "Content-Type:application/json"
