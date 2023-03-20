docker network create nonrtric-docker-net

echo "RIC Simulator"
docker run -d --rm -p 8085:8085 -p 8185:8185 -e A1_VERSION=OSC_2.1.0 -e ALLOW_HTTP=true --network=nonrtric-docker-net --name=ric1 nexus3.o-ran-sc.org:10002/o-ran-sc/a1-simulator:2.3.1
echo ""

echo "A1 policy Management Service"
docker run -d --rm -v $(HOME)/nonrtric_f_release/install/a1policymanagementservice/application_configuration_SDNC.json:/opt/app/policy-agent/data/application_configuration.json -p 8081:8081 -p 8433:8433 --network=nonrtric-docker-net --name=policy-agent-container nexus3.o-ran-sc.org:10002/o-ran-sc/nonrtric-plt-a1policymanagementservice:2.4.1

# echo ""
# 
# echo "SDNC A1 Controller"
# cd $(pwd)/sdnc_a1controller/
# docker-compose up -d
# cd $(pwd)/script

echo ""

echo "Information Coordinator Service"
docker run -d --rm -p 8083:8083 -p 8434:8434 --network=nonrtric-docker-net --name=information-coordinator-service nexus3.o-ran-sc.org:10002/o-ran-sc/nonrtric-plt-informationcoordinatorservice:1.3.1

echo ""

echo "Control Panel"
docker run -d --rm -v $(HOME)/nonrtric_f_release/install/control_panel/nginx.conf:/etc/nginx/nginx.conf -p 8080:8080 --network=nonrtric-docker-net --name=control-panel  nexus3.o-ran-sc.org:10002/o-ran-sc/nonrtric-controlpanel:2.3.0


echo ""

echo "Gateway"
docker run -d --rm -v $(HOME)/nonrtric_f_release/install/nonrtric_gateway/application.yaml:/opt/app/nonrtric-gateway/config/application.yaml -p 9090:9090 --network=nonrtric-docker-net --name=nonrtric-gateway  nexus3.o-ran-sc.org:10002/o-ran-sc/nonrtric-gateway:1.0.0

echo ""

echo "Dmaap Adapter Service"
docker run -d --rm \
-v $(HOME)/nonrtric_f_release/install/dmaap_adapter/application.yaml:/opt/app/dmaap-adaptor-service/config/application.yaml \
-v $(HOME)/nonrtric_f_release/install/dmaap_adapter/application_configuration.json:/opt/app/dmaap-adapter-service/data/application_configuration.json \
-p 9086:8084 -p 9087:8435 --network=nonrtric-docker-net --name=dmaap-adaptor-service  nexus3.o-ran-sc.org:10002/o-ran-sc/nonrtric-plt-dmaapadapter:1.1.1

echo ""

echo "Dmaap Mediator Producer"
docker run -d --rm -v \
$(HOME)/nonrtric_f_release/install/dmaap_mediator_producer/type_config.json:/configs/type_config.json \
-p 8885:8085 -p 8985:8185 --network=nonrtric-docker-net --name=dmaapmediatorservice \
-e "INFO_COORD_ADDR=https://information-coordinator-service:8434" \
-e "DMAAP_MR_ADDR=https://message-router:3905" \
-e "LOG_LEVEL=Debug" \
-e "INFO_PRODUCER_HOST=https://dmaapmediatorservice" \
-e "INFO_PRODUCER_PORT=8185" \
buld_producer_test:1.0.0

echo ""

echo "App Catalogue Service"
docker run -d --rm -p 8680:8680 -p 8633:8633 --network=nonrtric-docker-net --name=rapp-catalogue-service nexus3.o-ran-sc.org:10002/o-ran-sc/nonrtric-plt-rappcatalogue:1.1.0

echo ""

echo "deploy finish, please wait a moment to make sure container are ready"
sleep 30s
echo "checking for each container......................."
# sh check_deploy.sh

