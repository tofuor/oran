hostname=192.168.122.65
  
# uninstall old xapps
curl --location --request DELETE "http://$hostname:32080/appmgr/ric/v1/xapps/hw-cpp"
curl --location --request DELETE "http://$hostname:32080/appmgr/ric/v1/xapps/hw-python"
