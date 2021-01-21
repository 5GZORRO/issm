# python-kafka

Base image to be used by argo `produce` template defined in ISSM common templates library.
This image also contains the `requests` to be used by Argo steps/tasks to communicate with services via HTTP

## Build and push docker images (**relevant for developers only**)

1.  Set the `REGISTRY` environment variable to hold the name of your docker registry. The following command sets it
    equal to the docker github package repository.

    ```
    $ export REGISTRY=docker.pkg.github.com
    ```

1.  Set the `IMAGE` environment variable to hold the image of the operator.

    ```
    $ export IMAGE=$REGISTRY/5gzorro/issm/python:alpine3.6-kafka
    ```

1.  Invoke the below command.

    ```
    $ docker build --tag "$IMAGE" --force-rm=true .
    ```

1.  Push the image.

    ```
    $ docker push "$IMAGE"
    ```
