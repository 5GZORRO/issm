# Onboard Blueprint

Log into the vertical slicer host and perform the below in this order

## Clone this repository

```
cd ~
git clone https://github.com/5GZORRO/issm.git
cd issm/scripts/slicer
```

## Expose VNFD for the vertical slicer to consume

Tar the descriptor

```
tar -cvf vnfd01.tar vnfd01.json
```

Start nginx ..

```
docker run -it --rm -d -p 8080:80 --name web -v ${PWD}:/usr/share/nginx/html nginx
```

## Onboard VideoStreaming blueprint

Follow the below procedure to onboard the blueprint

### Set slicer ipaddress

Update ipadress to the one in your environment

```
export SLICER=10.4.3.10
```

### Customize VSB 

```
sed 's,%SLICER%,'${SLICER}',g' vsb_VideoStreaming.json.template > vsb_VideoStreaming.json
```

### Onboard it

```
./vsb_onboard.sh
```
