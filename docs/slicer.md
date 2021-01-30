# Vertical Slicer

**Note: This is a work in progress. Ensure to monitor this repository frequently**

Create Ubuntu 18.04 VMs with 2vCPUs 8GB RAM 100 GB disk

Log into the VM and perform the below instructions in the order they appear

## Clone repository

```
cd ~
git clone https://github.com/nextworks-it/slicer.git
cd slicer
```

## Configure slicer nfvo drivers

Configure slicer NFVO driver to use the `dummy` driver

edit `SEBASTIAN/src/main/resources/application.properties` and set the dummy driver

```
nfvo.type=DUMMY
```

## Install backend and UI

Follow instructions at [slicer readme](https://github.com/nextworks-it/slicer/blob/master/README.md)
