#!/bin/sh
docker build -t nexus3.o-ran-sc.org:10002/mitlab/python-ddqn-test:1.0.0 .

dms_cli uninstall python-ddqn-test ricxapp
dms_cli onboard config-file.json schema.json 
dms_cli install python-ddqn-test 1.0.0 ricxapp

kubectl get pod -n ricxapp
