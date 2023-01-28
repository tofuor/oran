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
	ricip: ""
	auxip: ""
```
## install NearRT
```
./install -f ../RECIPE_EXAMPLE/example_recipe_oran_f_release.yaml
```
### install xapp deploy tool
```
docker run --rm -u 0 -it -d -p 8090:8080 -e DEBUG=1 -e STORAGE=local -e STORAGE_LOCAL_ROOTDIR=/charts -v $(pwd)/charts:/charts chartmuseum/chartmuseum:latest
export CHART_REPO_URL=http://0.0.0.0:8090
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
