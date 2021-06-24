# Configure Kubernetes to use a private docker registry

## Log into private docker hub

Obtain Git token per [these instructions](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

Log into Git docker registry using your token

```
cat ~/TOKEN.txt | sudo docker login https://docker.pkg.github.com -u <git username> --password-stdin
```

After the login you should have `~/.docker/config.json` file created with the registry credentials


### Create kubernetes secrete file out from docker config file

`docker-secrete.yaml`

```
apiVersion: v1
kind: Secret
metadata:
  name: myregistrykey
data:
  .dockerconfigjson: <paste base64 encoded of ~/.docker/config.json>
type: kubernetes.io/dockerconfigjson
```

Create a file `docker-secrete.yaml` and paste your base64 encoded config.json file as described below

**Keep this file.. you will need it during the deployment of your kubernetes services**

**Tip:** you can use the below python snippet to encode docker config.json file

```
import base64

with open('/home/<replace user>/.docker/config.json', 'rb') as config_file:
    config_file_data = config_file.read()
    base64_encoded_data = base64.b64encode(config_file_data)
    base64_message = base64_encoded_data.decode('utf-8')

    print(base64_message)
```
