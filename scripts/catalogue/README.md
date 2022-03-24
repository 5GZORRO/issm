# Catalogue Endpoints for managing POs

Define your catalogue URL

```
export URL=http://172.28.3.126:31080
```

## Product Offer

### Get all productOfferings

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOffering" -H  "accept: application/json" | jq .
```

### List UPF productOfferings

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOffering" -H  "accept: application/json" | jq -r '.[] | select(.name=="free5gc UPF").id'
```

### Get specific productOffering

```
export ID=03f0f8a5-a785-4575-a608-ecf93b819153
```

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOffering/$ID" -H  "accept: application/json" | jq .
```

### Create productOffering

Customize `upf/payloads/productOffering.json` and set productSpecification, productOfferingPrice IDs

```
curl -X POST -d "@payloads/upf/productOffering.json" "$URL/tmf-api/productCatalogManagement/v4/productOffering" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```

### Delete productOffering

```
export ID=e67c4dbd-744e-4611-9269-17486f83cf48
```

```
curl -X DELETE "$URL/tmf-api/productCatalogManagement/v4/productOffering/$ID" -H  "accept: application/json" -H "Content-Type: application/json"
```

## Product Offer Price

### Create productOfferingPrice

```
curl -X POST -d "@payloads/upf/productOfferingPrice.json" "$URL/tmf-api/productCatalogManagement/v4/productOfferingPrice" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```

### List UPF productOfferingPrice

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOfferingPrice" -H  "accept: application/json" | jq -r '.[] | select(.name=="free5gc UPF - pricing").id'
```


## Product Specification

### Get all productSpecifications

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productSpecification" -H  "accept: application/json" | jq .
```

### List UPF productSpecifications

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productSpecification" -H  "accept: application/json" | jq -r '.[] | select(.name=="free5gc UPF").id'
```


### Get specific productSpecification

```
export ID=03f0f8a5-a785-4575-a608-ecf93b819153
```

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productSpecification/$ID" -H  "accept: application/json" | jq .
```

### Create productSpecification

Customize `upf/payloads/productSpecification.json` and set resourceSpecification ID

```
curl -X POST -d "@payloads/upf/productSpecification.json" "$URL/tmf-api/productCatalogManagement/v4/productSpecification" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```

### Delete productSpecification

```
export ID=e67c4dbd-744e-4611-9269-17486f83cf48
```

```
curl -X DELETE "$URL/tmf-api/productCatalogManagement/v4/productSpecification/$ID" -H  "accept: application/json" -H "Content-Type: application/json"
```

## Resource Specification

### Get all resourceSpecifications

```
curl -X GET "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" | jq .
```

### List UPF resourceSpecifications

```
curl -X GET "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" | jq -r '.[] | select(.name=="free5gc UPF").id'
```

### Get specific resourceSpecification

```
export ID=03f0f8a5-a785-4575-a608-ecf93b819153
```

```
curl -X GET "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification/$ID" -H  "accept: application/json" | jq .
```

### Create resourceSpecification

Customize `upf/payloads/resourceSpecification.json`

```
curl -X POST -d "@payloads/upf/resourceSpecification.json" "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```

### Delete resourceSpecification

```
export ID=e67c4dbd-744e-4611-9269-17486f83cf48
```

```
curl -X DELETE "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification/$ID" -H  "accept: application/json" -H "Content-Type: application/json"
```
