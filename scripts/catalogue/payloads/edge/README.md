# Catalogue Endpoints for managing Edge POs

This page summarizes (bottom up) the steps to define resource specification, offer specification, pop, and product offer

* Create resourceSpecification: [here](./README.md#create-resourcespecification)
* Create productSpecification: [here](./README.md#create-productspecification)
* Create productOfferingPrice: [here](./README.md#create-productofferingprice)
* Create productOffering: [here](./README.md#create-productoffering)

Throughout the steps define your catalogue URL

**Note:** the below points to 3rd party domain's catalogue

**Use the portal UI to create the offer itself**

```
export URL=http://172.28.3.126:32080
```

## Product Offer

### List Core productOfferings

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOffering" -H  "accept: application/json" | jq -r '.[] | select(.name=="IaaS Edge Resource").id'
```

## Product Offer Price

### Create productOfferingPrice

```
curl -X POST -d "@productOfferingPrice.json" "$URL/tmf-api/productCatalogManagement/v4/productOfferingPrice" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```

### List Core productOfferingPrice

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productOfferingPrice" -H  "accept: application/json" | jq -r '.[] | select(.name=="IaaS Edge Resource - pricing").id'
```

## Product Specification

### List Core productSpecifications

```
curl -X GET "$URL/tmf-api/productCatalogManagement/v4/productSpecification" -H  "accept: application/json" | jq -r '.[] | select(.name=="IaaS Edge Resource").id'
```

## Resource Specification

### List Core resourceSpecifications

```
curl -X GET "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" | jq -r '.[] | select(.name=="IaaS Edge Resource").id'
```

### Create resourceSpecification

Customize `resourceSpecification.json`

```
curl -X POST -d "@resourceSpecification.json" "$URL/tmf-api/resourceCatalogManagement/v2/resourceSpecification" -H  "accept: application/json" -H "Content-Type: application/json" | jq -r .id
```
