# Catalogue Endpoints for managing POs

This page summarizes (bottom up) the steps to define resource specification, offer specification, pop, and product offer

* Create resourceSpecification: [here](./README.md#create-resourcespecification)
* Create productSpecification: [here](./README.md#create-productspecification)
* Create productOfferingPrice: [here](./README.md#create-productofferingprice)
* Create productOffering: [here](./README.md#create-productoffering)

Throughout the steps define your catalogue URL

```
export URL=http://172.28.3.126:31080
```

**NOTE:** update ID variable accordingly per the below curls

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

**Important: register your offer with elicensing service**

update values (URL, productId, nsDescriptorId) accordingly

```
curl -X POST  --header "Content-Type:application/json"  -d '{"productId": "2a8ffjFXUdX4ciQd1e9dZa", "nsDescriptorId": "fiveg-subnet", "nsInstanceId": ""}' http://172.28.3.42:31880/checkLicensing | jq .
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

### Get specific productOfferingPrice

```
export ID=03f0f8a5-a785-4575-a608-ecf93b819153
```

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOfferingPrice/$ID" -H  "accept: application/json" | jq .
```

### Delete productOfferingPrice

```
export ID=03f0f8a5-a785-4575-a608-ecf93b819153
```

```
curl -X DELETE "$URL/tmf-api/productCatalogManagement/v4/productOfferingPrice/$ID" -H  "accept: application/json"
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

## Product Offer status

### Get specific productOfferingStatus

```
export ID=e67c4dbd-744e-4611-9269-17486f83cf48
```

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOfferingStatus/$ID" -H  "accept: application/json" | jq .
```
