# oran

mitlab B5G group

## install Non-RT RIC f release with docker

### 1. env setting

```
    cd ${HOME}/nonrtric_f_release/install/script/
    nano deploy_nonrtric.sh


    NearRT=<Near Real Time RIC IP>
    ONAP_IP=<ONAP IP>
    ...
```

### 2. deploy service

```
    cd $(HOME)/nonrtric_f_release/install/script
    sudo sh deploy_nonrtric.sh
```

### 3. deploy rapp

```
    cd $(HOME)/nonrtric_f_release/rapp/rApp_A1_test
    sudo sh build_rapp.sh
```
## other package
### 1. install grafana
```
    docker pull grafana/grafana:latest
    mkdir /var/lib/grafana -p

    docker run -d -p 3000:3000 -v /var/lib/grafana:/var/lib/grafana -e "GF_SECURITY_ADMIN_PASSWORD=mitlab" grafana/grafana
```
### 2. install elasticsearch
```
    sudo mkdir -p /usr/local/logstash/conf.d
    sudo mkdir -p /usr/local/logstash/coadnfig
    sudo mkdir -p /usr/local/logstash/logs

    sudo chmod -777 /usr/local/logstash
    nano /usr/local/logstash/logstash.yml

    docker run -d -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" --name elasticsearch --net nonrtric-docker-net -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.5.1
```

```
    docker run -d --name kibana --net nonrtric-docker-net -p 5601:5601 docker.elastic.co/kibana/kibana:7.4.2
```