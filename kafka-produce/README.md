# python-kafka

Base image used by ISSM `produce` template defined in common templates library. This image contains python `requests` library to be used by ISSM workflow to communicate with services via HTTP.

## Build and push docker images (**relevant for developers only**)

1.  Set the `REGISTRY` environment variable to hold the name of your docker registry. The following command sets it
    equal to the docker github package repository.

    ```
    $ export REGISTRY=docker.pkg.github.com
    ```

1.  Set the `IMAGE` environment variable to hold the image of the operator.

    ```
    $ export IMAGE=$REGISTRY/5gzorro/issm/python:alpine3.6-kafka-v0.1
    ```

1.  Invoke the below command.

    ```
    $ docker build --tag "$IMAGE" --force-rm=true .
    ```

1.  Push the image.

    ```
    $ docker push "$IMAGE"
    ```
