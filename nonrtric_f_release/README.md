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