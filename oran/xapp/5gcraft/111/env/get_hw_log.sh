#!/bin/sh
hw=$(kubectl get pods -n ricxapp | grep hw | awk '{print$1}')
  
kubectl logs $hw -n ricxapp
