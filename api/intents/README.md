# ISSM intents

An ISSM intent defines the input parameters (json) to be used when submitting a new transaction

## Intent structure

An ISSM intent consists of two sections

### Generic section

Generic attributes that exist on every intent

* `operation`: the type of the transaction (str) (e.g. 'instantiate', 'scaleout')
* `order_id`: the identifiers of orders that the transaction will operate on. There should be a single main order and additional (optional) sub orders (json list)
* `place`: the location (in trmf format) of where to search for available resources (json) (applicable for 'scaleout' transaction)

### Specific section

Specific attributes processed by the s-nfvo

* `snfvo_data`: key, val pairs (json) known to the s-nfvo

**Note:** additional key, val pair are automatically added by ISSM. These are the sub orders ids (if exist) in the following format: `<sub order offer category>_order_id_<index>`

## Intent examples

Various ISSM intents had been defined to support the three 5GZorro Use-cases

They can be found in the underlying sub-folders