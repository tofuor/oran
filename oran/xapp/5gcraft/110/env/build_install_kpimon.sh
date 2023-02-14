#!/bin/sh
dms_cli uninstall kpimon ricxapp
dms_cli onboard ./config_server/kpimon/config.json schema.json 
dms_cli install kpimon 1.1.0 ricxapp

kubectl get pod -n ricxapp
