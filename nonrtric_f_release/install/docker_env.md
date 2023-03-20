# container env
## Real Near-RT RIC
```
NEAR_RT_RIC="192.168.122.65" 
```
## Near-RT RIC simulator
```
SIMULATOR_container_name="ric1"  
SIMULATOR_PORT1=8085  
SIMULATOR_PORT2=8185
```
## A1_MEDIATOR_PORT=0
```

```
## A1 policy management service
```
A1_POLICY_AGENT_container_name="policy-agent-container"  
A1_POLICY_AGENT_PORT1=8081  
A1_POLICY_AGENT_PORT2=8433
```
## Information coordinator service
```
ICS_container_name="information-coordinator-service"  
ICS_PORT1=8083  
ICS_PORT2=8434  
```
## Control panel
```
CONTROL_PANEL_container_name="control-panel"  
CONTROL_PANEL_PORT=8080  
```
## Non-RT RIC gateway
```
NONRTRIC_GATEWAY_container_name="nonrtric-gateway"  
NONRTRIC_GATEWAY_PORT=9090  
```
## Dmaap adaptor service
```
DMAAP_ADAPTER_container_name="dmaap-adaptor-service"  
temp_DMAAP_ADAPTER_PORT1=9086  
DMAAP_ADAPTER_PORT1=8084  
temp_DMAAP_ADAPTER_PORT2=9087  
DMAAP_ADAPTER_PORT2=8435  
```
## Dmaap mediator producer
```
DMAAP_MEDIATOR="dmaapmediatorservice"  
temp_DMAAP_MEDIATOR_PORT1=8885  
DMAAP_MEDIATOR_PORT1=8085  
temp_DMAAP_MEDIATOR_PORT2=8985  
DMAAP_MEDIATOR_PORT2=8185  
```
## app catalogue sevice
```
APP_CATALOGUE="rapp-catalogue-service"  
APP_CATALOGUE_PORT1=8680  
APP_CATALOGUE_PORT2=8633
```