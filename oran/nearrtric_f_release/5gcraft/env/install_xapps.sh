hostname=192.168.0.28

# uninstall old xapps
curl --location --request DELETE "http://$hostname:32080/appmgr/ric/v1/xapps/kpimon"
curl --location --request DELETE "http://$hostname:32080/appmgr/ric/v1/xapps/ts"

# install xapps to appmgr
curl --location --request POST "http://$hostname:32080/onboard/api/v1/onboard/download"      --header 'Content-Type: application/json' --data-binary "@./onboard.ts.url"
curl --location --request POST "http://$hostname:32080/onboard/api/v1/onboard/download"      --header 'Content-Type: application/json' --data-binary "@./onboard.kpimon.url"
# checking what have been on-boarded
curl --location --request GET "http://$hostname:32080/onboard/api/v1/charts"

# install helm charts from appmgr
curl --location --request POST "http://$hostname:32080/appmgr/ric/v1/xapps"      --header 'Content-Type: application/json' --data-raw '{"xappName": "ts"}'
curl --location --request POST "http://$hostname:32080/appmgr/ric/v1/xapps"      --header 'Content-Type: application/json' --data-raw '{"xappName": "kpimon"}'
# now check the running state of these xApps
kubectl get pods -n ricxapp
