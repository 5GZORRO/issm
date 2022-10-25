## Define environment variables

Define your catalogue URL

```
export URL=http://172.28.3.15:31080
```

**Notes:**

* it is assumed that the names do not exist and unique
* service specification should already contain the correct related party info

## Create resourceSpecification

```
curl -X POST -d "@resourceSpecification-core.json" "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
curl -X POST -d "@resourceSpecification-upf.json" "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
curl -X POST -d "@resourceSpecification-vcache.json" "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```

## Customize network service

```
coreId=`curl $URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification -H  "accept: application/json" -H "Content-Type: application/json" | jq -r '.[] | select(.name=="core")'.id`

upfId=`curl $URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification -H  "accept: application/json" -H "Content-Type: application/json" | jq -r '.[] | select(.name=="upf")'.id`

vcacheId=`curl $URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification -H  "accept: application/json" -H "Content-Type: application/json" | jq -r '.[] | select(.name=="vcache")'.id`
```

```
sed -i "s|%url%|$URL|g" my_service_spec.json
sed -i "s/%coreId%/$coreId/g" my_service_spec.json
sed -i "s/%upfId%/$upfId/g" my_service_spec.json
sed -i "s/%vcacheId%/$vcacheId/g" my_service_spec.json
```

## Create network service

```
curl -X POST -d "@my_service_spec.json" "$URL/tmf-api/serviceCatalogManagement/v4/serviceSpecification" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```
