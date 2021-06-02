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

Set the ipadress of your nginx container. **Note:** it should be the external ipaddress so that the VS can access it

```
export NGINX_URL=172.15.0.191:8080
```

### Customize VSB 

```
sed 's,%NGINX_URL%,'${NGINX_URL}',g' vsb_VideoStreaming.json.template > vsb_VideoStreaming.json
```

### Onboard it

```
export SLICER_URL=172.15.0.191:8082
./vsb_onboard.sh
```
