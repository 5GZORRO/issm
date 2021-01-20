# Argo installation instructions

Instructions assume you already have a kubernetes cluster provisioned. You can use [these instructions](https://github.ibm.com/5g-zorro/infrastructure/blob/master/docs/kubernetes.md) to provision such a one

## Argo workflow engine

Log into kubernetes master

Commands below are taken from [here](https://github.com/argoproj/argo/releases/tag/v2.12.0-rc3)

### Argo CLI

```
curl -sLO https://github.com/argoproj/argo/releases/download/v2.12.0-rc3/argo-linux-amd64.gz
gunzip argo-linux-amd64.gz
chmod +x argo-linux-amd64
sudo mv ./argo-linux-amd64 /usr/local/bin/argo
# test installation
argo version
```

### Argo controller

```
kubectl create namespace argo
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo/v2.12.0-rc3/manifests/install.yaml
```

### Configure service account

```
kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=default:default
```

### Validate install

Submit hello-world workflow

```
argo submit --watch https://raw.githubusercontent.com/argoproj/argo/master/examples/hello-world.yaml
```

Retrieve its logs

```
argo logs -n argo @latest
```

### Argo UI

In a different terminal, log into kubernetes master and invoke the below to start the UI

```
argo server
```

Ensure you can access the UI by browsing `http://localhost:2746`

## Argo events

Log into kubernetes master

Commands below are taken from [here](https://argoproj.github.io/argo-events/installation)

### Controllers

```
kubectl create namespace argo-events
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/v1.1.0/manifests/install.yaml
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/v1.1.0/examples/eventbus/native.yaml
```

