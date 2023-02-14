#!/bin/sh
docker build -t nexus3.o-ran-sc.org:10002/mitlab/ric-app-python-savedata:1.0.0 .

dms_cli uninstall python-savedata ricxapp
dms_cli onboard config-file.json schema.json 
dms_cli install python-savedata 1.0.0 ricxapp

kubectl get pod -n ricxapp