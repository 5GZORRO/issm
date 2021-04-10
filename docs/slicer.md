# Vertical Slicer

**Note: This is a work in progress. Ensure to monitor this repository frequently**

Create Ubuntu 18.04 VMs with 2vCPUs 8GB RAM 100 GB disk

Log into the VM and perform the below instructions in the order they appear

## Clone repository

```
cd ~
git clone https://github.com/nextworks-it/slicer.git
cd slicer
git checkout feat-5gzorro-hackathon
cd INSTALL/vertical-slicer-docker
```

**Note:** End to end tests use VS with commit id: a6ff0d8

## Configure external ipaddress

edit `environment/environments.ts` and replace with VM ipaddress

```
 baseUrl: 'http://<slicer external ipaddress>:8082/'
```

## Configure slicer nfvo and monitoring drivers

Configure slicer NFVO/monitoring to `dummy` and `MDA`

edit `sebastian/sebastian_application.properties` with the below.

**Note:** Update external_monitoring address with the host MDA is deployed

```
nfvo.lcm.type=DUMMY

nfvo.lcm.external_monitoring.enable=true
nfvo.lcm.external_monitoring.type=MDA
domain_id=operator-a-in-0
nfvo.lcm.external_monitoring.address=http://172.15.0.191:4000
```

## Start the slicer

**Note:** first run takes some time as the images get built

```
docker-compose up
```

## Browse to its GUI

Point your browser to `http://<slicer external ipaddress>`

Log in with `admin`/`admin`
