# isbp

## Test sla-event publication

**Note:** it is assumed that topic `isbp-topic` already exists in DL kafka

Log into kubernetes master where ISSM is running

Invoke the below to publish "sla-event" into DL kafka (update flow parameters accordingly)

```
argo submit ./sla-event.yaml -n argo-events
```

Log into DL kafka host

```
~/kafka_2.13-2.7.0/bin/kafka-console-consumer.sh --bootstrap-server 172.28.3.196:9092 --topic isbp-topic --from-beginning
```

```
{"data": {"eventType": "new_SLA", "transactionID": "123", "productID": "456", "resourceID": "789", "instanceID": "10"}}
```