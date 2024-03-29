# isbp

## Emulate sla-event publication

Test script to emulate sending an SLA event to ISBP component.

**Note:** it is assumed that topic `isbp-topic` already exists in DL kafka

Log into kubernetes master where ISSM is running

## via flow

Invoke the below to publish "sla-event" into DL kafka (update flow parameters accordingly)

```
argo submit ./sla-event.yaml -n issm
```

## manual publish

Log into DL kafka host

```
~/kafka_2.13-2.7.0/bin/kafka-console-consumer.sh --bootstrap-server 172.28.3.196:9092 --topic isbp-topic --from-beginning
```

```
{"data": {"eventType": "new_SLA", "transactionID": "aaefbe5e7024466bbc88f28e60afb5ab", "productID": "PAnTByduyWkFJcoqsurweZ", "SLAID": "V7qnCySru2jdDEjbXpERaB", "instanceID": "37", "kafka_ip": "172.28.3.196", "kafka_port": "9092", "topic": "isbp-topic-out"}}
```

## Emulate sla-breach notification

Test script to emulate sending an SLA breach notification to ISSM.

**Note:** it is assumed that topic `isbp-topic-out` already exists in ISSM kafka

Log into kubernetes master where ISSM is running

## via flow

Invoke the below to publish "sla-event" into DL kafka (update flow parameters accordingly)

```
argo submit ./sla-breach.yaml -n issm
```
