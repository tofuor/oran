#!/bin/sh

sudo docker build --network=host . -t nexus2.o-ran-sc.org:10002/idb-contest/ric-app-ts:0.0.2
