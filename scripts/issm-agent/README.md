# scripts/issm-agent

Log into a VM that has a connectivity to ISSM Kafka (see [pre-requisites](https://github.com/5GZORRO/issm#pre-requisites))

## Actuator Agent

Setup an actuator agent. This part consists of an actuation code that publishes an intent to ISSM Workflow manager to consume and run a codified business flow for it

### Clone this repository

```
cd ~
git clone https://github.com/5GZORRO/issm.git
cd issm/scripts/issm-agent
```

### Configure pip

```
sudo apt install python3-venv python3-pip
```

```
python3 -m pip install --user --upgrade pip
```

### Virtual environment

```
python3 -m venv ~/virtual/environment-agent
```

### Install & launch the agent

```
source ~/virtual/environment-agent/bin/activate
pip3 install gevent==1.2.1 kafka-python==2.0.2
```

```
python3 ./agent.py <TBD params>
```
