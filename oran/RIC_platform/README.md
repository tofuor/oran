## pre-install
```
git clone "https://gerrit.o-ran-sc.org/r/ric-plt/ric-dep"
cd ric-dep/bin
./install_k8s_and_helm.sh
./install_common_templates_to_helm.sh
```
add ip address
```
nano ric-dep/RECIPE_EXAMPLE/example_recipe_oran_f_release.yaml
```
```
extsvcplt:
	ricip: "insert your IP"
	auxip: "insert your IP"
```
## install NearRT
```
./install -f ../RECIPE_EXAMPLE/example_recipe_oran_f_release.yaml
```
### install chartmuseum
```
docker run --rm -u 0 -it -d -p 8090:8080 -e DEBUG=1 -e STORAGE=local -e STORAGE_LOCAL_ROOTDIR=/charts -v $(pwd)/charts:/charts chartmuseum/chartmuseum:latest
export CHART_REPO_URL=http://0.0.0.0:8090
```
### install xapp deploy tool
```
git clone "https://gerrit.o-ran-sc.org/r/ric-plt/appmgr"
cd appmgr/xapp_orchestrater/dev/xapp_onboarder
apt install python3-pip
pip3 uninstall xapp_onboarder
pip3 install ./
```
## deploy xapp example
```
cd xapp/xApp_example/xApp_example/init
dms_cli onboard /files/config-file.json /files/schema.json
```
List all the helm charts from help repository
```
curl -X GET http://localhost:8080/api/charts | jq .
```
```
dms_cli install iii-python 1.0.0 ricxapp
```

## debug
### 1.K8s SCTP error (fixed) 
```
Error: Service "service-ricplt-e2term-sctp-alpha" is invalid: spec.ports[0].protocol: Unsupported value: "SCTP": supported values: "TCP", "UDP"
```
#### fixed below
```
nano /etc/kubernetes/manifests/kube-apiserver.yaml
```
add " - --feature-gates=SCTPSupport=True " in command
```
...

- command:
    - kube-apiserver
    - --advertise-address=192.168.122.65
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --enable-admission-plugins=NodeRestriction
    - --enable-bootstrap-token-auth=true
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
    - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
    - --etcd-servers=https://127.0.0.1:2379
    - --feature-gates=SCTPSupport=True
    - --insecure-port=0
  
  ...
```
>>>>>>> f9664ca89e08fb45cda09f94bf1e548a6ee66566
=======
>>>>>>> f9664ca89e08fb45cda09f94bf1e548a6ee66566
