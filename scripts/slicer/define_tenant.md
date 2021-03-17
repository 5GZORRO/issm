# Define vertical tenant

Log into the vertical slicer host and perform the below in this order

### Clone this repository

```
cd ~
git clone https://github.com/5GZORRO/issm.git
cd issm/scripts/slicer
```

### Set slicer ipaddress

Update ipadress to the one in your environment

```
export SLICER=10.30.8.55
```

### Set tenant name

```
export GROUP=5gzorro
export TENANT=operator-a
```

### Define tenant SLA

```
export CPU=10
export RAM=10240
export STORAGE=100
```

### Create it

```
./tenant_create.sh
```
