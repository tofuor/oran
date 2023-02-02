#!/bin/sh

sudo docker build --network=host . -t nexus3.o-ran-sc.org:10002/o-ran-sc/ric-app-ts:0.0.2

dms_cli uninstall ts ricxapp
dms_cli onboard xapp-descriptor/config.json schema.json 
dms_cli install ts 0.0.2 ricxapp

kubectl get pod -n ricxapp