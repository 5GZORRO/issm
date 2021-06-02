# Onboard Blueprint

Log into the vertical slicer host and perform the below in this order

## Clone this repository

```
cd ~
git clone https://github.com/5GZORRO/issm.git
cd issm/scripts/slicer
```

## Expose VNFD for the vertical slicer to consume

### Tar the descriptor

```
tar -cvf vnfd01.tar vnfd01.json
```

### Start nginx..

Locally

```
docker run -it --rm -d -p 8080:80 --name web -v ${PWD}:/usr/share/nginx/html nginx
```

Or in kubernetes, following with copying the tar to nginx

```
kubectl create deployment vs-nginx --image=nginx
```

```
cp ./vnfd01.tar vs-nginx-6b98fbb698-rr6zx:/usr/share/nginx/html
```

## Onboard VideoStreaming blueprint

Follow the below procedure to onboard the blueprint

### Set slicer ipaddress

Set the ipadress of your nginx container/pod. **Note:** VS should be able to access it

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
