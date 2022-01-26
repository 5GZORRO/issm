## Intent - example

Scaleout intent contains the following data.

* intent_query - high level query intent to be used for the scaleout operation
* category     - the category of which the scaleout operation is to be considered
    * service  - scale out a service which its characteristics provided in the intent
    * resource - scale out a service which its IaaS requirements provided in the intent

Payload examples:

* [service level intent](./intent-service.json)
* [resource level intent](./intent-resource.json)
