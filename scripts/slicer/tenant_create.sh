#!/bin/bash

#
# Helper script to create a given tenant.
#

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
echo "Create group $GROUP"
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

curl  -X POST -d username=admin -d password=admin -c /tmp/a_c http://$SLICER:8082/login
curl  -b /tmp/a_c --write-out '%{http_code}' -X POST http://$SLICER:8082/vs/admin/group/$GROUP --header "Content-Type:application/json"

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Create tenant"
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

generate_post_tenant_create()
{
cat <<EOF
  {
    "username": "$TENANT",
    "password": "$TENANT"
  }
EOF
}
curl -b /tmp/a_c --write-out '%{http_code}' -X POST http://$SLICER:8082/vs/admin/group/$GROUP/tenant --data "$(generate_post_tenant_create)" --header "Content-Type:application/json"

sleep $BETWEEN
echo ""
echo ""
echo "-=-=-=-=-=-= TRACE -=-=-=-=-=-=-=-=-=-"
echo "Create SLA"
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-"

generate_post_sla_create()
{
  cat <<EOF
  {
    "slaStatus": "ENABLED",
    "slaConstraints": [{
      "maxResourceLimit": {
        "diskStorage": $STORAGE,
        "vCPU": $CPU,
        "memoryRAM": $RAM
        },
      "scope": "GLOBAL_VIRTUAL_RESOURCE"
    }]
  }
EOF
}

curl -b /tmp/a_c --write-out '%{http_code}' --data "$(generate_post_sla_create)" -X POST http://$SLICER:8082/vs/admin/group/$GROUP/tenant/$TENANT/sla --header "Content-Type:application/json"
