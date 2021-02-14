# scripts/actuator

Log into a VM that has a connectivity to ISSM Kafka (see [pre-requisites](https://github.com/5GZORRO/issm#pre-requisites))

## Actuator

Setup the actuator which consists an invoker that publishes an intent to ISSM Workflow manager to consume and run a codified business flow for it.

Currently the following intent operation is supported:

* `submit_intent`

### Clone this repository

```
cd ~
git clone https://github.com/5GZORRO/issm.git
cd issm/scripts/actuator
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

### Install

```
source ~/virtual/environment-agent/bin/activate
pip3 install gevent==1.2.1 kafka-python==2.0.2
```

### Launch the actuator

`slice_intent.json`

```
{
    "offered_price": "1700",
    "latitude": "56",
    "longitude": "5",
    "slice_segement": "edge",
    "category": "VideoStreaming",
    "qos_parameters": {
        "bandwidth": "30"
    }
}
```

Create `slice_intent.json` with the above content

Run the below updating kafka_ip with ISSM Kafka ipaddress

```
python agent.py --kafka_ip 10.20.3.4 --intent_file ./slice_intent.json --service_owner my-mno
```

You should receive asynch callback notifications for this intent flow
