#!/bin/bash

export SLICER="localhost"
export TENANT="weit"
export BETWEEN=3

generate_post_tenant_create()
{
  cat <<EOF
{
        "username": "$TENANT",
        "password": "$TENANT"
}
EOF
}

generate_post_vsd_create()
{
  cat <<EOF
{
        "vsd":{
                "name":"VSD_CDN_small",
                "version":"0.1",
                "vsBlueprintId":"5",
                "sst":"EMBB",
                "managementType":"PROVIDER_MANAGED",
                "qosParameters":{
                        "users":"1000"
                }
        },
        "tenantId":"$TENANT",
        "isPublic":true
}
EOF
}

generate_post_vsi_create()
{
  cat <<EOF
{
        "name": "VideoStreaming_edge",
	    "vsdId": "50",
	    "tenantId": "$TENANT"
}
EOF
}


echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Login admin.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -i -X POST -d username=admin -d password=admin -c admin_credentials http://$SLICER:8082/login 2>/dev/null

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Create Vertical Blueprint.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b admin_credentials -d "@$(pwd)/vsb_test_nbi_no_nsd.json" -X POST http://$SLICER:8082/vs/catalogue/vsblueprint --header "Content-Type:application/json" 2>/dev/null

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Create Vertical Tenant.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b admin_credentials -X POST http://$SLICER:8082/vs/admin/group/user/tenant --data "$(generate_post_tenant_create)" --header "Content-Type:application/json" 2>/dev/null

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Retrieve Tenant.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b admin_credentials http://$SLICER:8082/vs/admin/group/user/tenant/weit --header "Content-Type:application/json" 2>/dev/null | jq .

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Login to tenant.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -i -X POST -d username=$TENANT -d password=$TENANT -c tenant_credentials http://$SLICER:8082/login 2>/dev/null

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "List Vertical Blueprints.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b admin_credentials http://$SLICER:8082/vs/catalogue/vsblueprint --header "Content-Type:application/json" 2>/dev/null | jq .

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Create Vertical Slice Descriptor.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b tenant_credentials --data "$(generate_post_vsd_create)" -X POST http://$SLICER:8082/vs/catalogue/vsdescriptor --header "Content-Type:application/json" 2>/dev/null

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "List Vertical Slice Descriptors.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b tenant_credentials http://$SLICER:8082/vs/catalogue/vsdescriptor --header "Content-Type:application/json" 2>/dev/null

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Instantiate Vertical Slice Descriptor.."
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl -b tenant_credentials --data "$(generate_post_vsi_create)" -X POST http://$slicer:8082/vs/basic/vslcm/vs --header "Content-Type:application/json" 2>/dev/null
