# Catalogue Endpoints for managing POs

Define your catalogue URL

```
export URL=http://172.28.3.126:31080
```

## Product Offer

### Get all product offers

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOffering" -H  "accept: application/json" | jq .
```

### Get specific product offer

```
export ID=03f0f8a5-a785-4575-a608-ecf93b819153
```

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOffering/$ID" -H  "accept: application/json" | jq .
```

## Product Specification

### Get all productSpecifications

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productSpecification" -H  "accept: application/json" | jq .
```

### Get specific productSpecification

```
export ID=03f0f8a5-a785-4575-a608-ecf93b819153
```

```
curl -X GET "$URL/tmf-api/resourceCatalogManagement/v4/productSpecification/$ID" -H  "accept: application/json" | jq .
```

## Resource Specification

### Get all resourceSpecifications

```
curl -X GET "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" | jq .
```

### Get specific resourceSpecification

```
export ID=03f0f8a5-a785-4575-a608-ecf93b819153
```

```
curl -X GET "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification/$ID" -H  "accept: application/json" | jq .
```

### Create resourceSpecification

```
curl -X POST -d "@payloads/resourceSpecification.json" "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```

### Delete resourceSpecification

```
export ID=e67c4dbd-744e-4611-9269-17486f83cf48
```

```
curl -X DELETE "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification/$ID" -H  "accept: application/json" -H "Content-Type: application/json"
```
