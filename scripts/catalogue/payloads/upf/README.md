# Catalogue Endpoints for managing UPF POs

This page summarizes (bottom up) the steps to define resource specification, offer specification, pop, and product offer

* Create resourceSpecification: [here](./README.md#create-resourcespecification)
* Create productSpecification: [here](./README.md#create-productspecification)
* Create productOfferingPrice: [here](./README.md#create-productofferingprice)
* Create productOffering: [here](./README.md#create-productoffering)

Throughout the steps define your catalogue URL

```
export URL=http://172.28.3.15:31080
```

## Product Offer

### List UPF productOfferings

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOffering" -H  "accept: application/json" | jq -r '.[] | select(.name=="free5gc UPF").id'
```


### Create productOffering

Customize `productOffering.json` and set productSpecification, productOfferingPrice IDs

```
curl -X POST -d "@productOffering.json" "$URL/tmf-api/productCatalogManagement/v4/productOffering" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```

**Important: register your offer with elicensing service**

update values (URL, productId, nsDescriptorId) accordingly

```
curl -X POST  --header "Content-Type:application/json"  -d '{"productId": "2a8ffjFXUdX4ciQd1e9dZa", "nsDescriptorId": "fiveg-subnet", "nsInstanceId": ""}' http://172.28.3.42:31880/checkLicensing | jq .
```

## Product Offer Price

### Create productOfferingPrice

```
curl -X POST -d "@productOfferingPrice.json" "$URL/tmf-api/productCatalogManagement/v4/productOfferingPrice" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```

### List UPF productOfferingPrice

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOfferingPrice" -H  "accept: application/json" | jq -r '.[] | select(.name=="free5gc UPF - pricing").id'
```

## Product Specification

### List UPF productSpecifications

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productSpecification" -H  "accept: application/json" | jq -r '.[] | select(.name=="free5gc UPF").id'
```

### Create productSpecification

Customize `productSpecification.json` and set resourceSpecification ID

```
curl -X POST -d "@productSpecification.json" "$URL/tmf-api/productCatalogManagement/v4/productSpecification" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```

## Resource Specification

### List UPF resourceSpecifications

```
curl -X GET "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" | jq -r '.[] | select(.name=="free5gc UPF").id'
```

### Create resourceSpecification

Customize `resourceSpecification.json`

```
curl -X POST -d "@resourceSpecification.json" "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```
