hostname=192.168.122.65

# uninstall old xapps
curl --location --request DELETE "http://$hostname:32080/appmgr/ric/v1/xapps/ts"

# install xapps to appmgr
curl --location --request POST "http://$hostname:32080/onboard/api/v1/onboard/download"      --header 'Content-Type: application/json' --data-binary "@./onboard.ts.url"
# checking what have been on-boarded
curl --location --request GET "http://$hostname:32080/onboard/api/v1/charts"

# install helm charts from appmgr
curl --location --request POST "http://$hostname:32080/appmgr/ric/v1/xapps"      --header 'Content-Type: application/json' --data-raw '{"xappName": "ts"}'
# now check the running state of these xApps
kubectl get pods -n ricxapp


# # uninstall old xapps
# curl --location --request DELETE "http://192.168.122.65:32080/appmgr/ric/v1/xapps/ts"

# # install xapps to appmgr
# curl --location --request POST "http://192.168.122.65:32080/onboard/api/v1/onboard/download"      --header 'Content-Type: application/json' --data-binary "@./onboard.ts.url"
# # checking what have been on-boarded
# curl --location --request GET "http://192.168.122.65:32080/onboard/api/v1/charts"

# # install helm charts from appmgr
# curl --location --request POST "http://192.168.122.65:32080/appmgr/ric/v1/xapps"      --header 'Content-Type: application/json' --data-raw '{"xappName": "ts"}'
# # now check the running state of these xApps
# kubectl get pods -n ricxapp
