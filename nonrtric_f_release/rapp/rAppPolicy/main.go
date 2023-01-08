package main

import (
	"log"
	"rAppPolicy/pkg/request"
	"time"
)

type Policy struct {
	Ric_id                  string         `json:"ric_id"`
	Policy_id               string         `json:"policy_id"`
	Service_id              string         `json:"service_id"`
	Policytype_id           string         `json:"policytype_id"`
	Status_notification_uri string         `json:"status_notification_uri"`
	Policy_data             map[string]any `json:"policy_data"`
	Transient               bool           `json:"transient"`
	// Status                  map[string]any `json:"status"`
	// Last_modified           string         `json:"last_modified"`
}

func main() {
	// create policy
	// set baseurl and api path
	baseurl := "http://192.168.122.35:9090"
	apipath := "/a1-policy/v2/policies"

	policy := Policy{}
	policy.Ric_id = "ric2"
	policy.Policy_id = "422522d3-2b60-44b3-b7db-cdef6fb4df22" // UUID
	policy.Service_id = "control-panel"
	policy.Policytype_id = "1"
	policy.Policy_data = make(map[string]any)
	policy.Transient = false

	// create policy
	log.Printf("Create Policy %s", policy.Policy_id)
	request := request.Request{}
	resp_create, err_create := request.Put(baseurl, apipath, policy)
	if err_create != nil {
		log.Println(err_create)
	}

	resp_create.RespPrint()

	log.Println("wait 30s......")
	time.Sleep(30 * time.Second)

	// get policy information
	apipath_get_info := apipath + "/" + policy.Policy_id
	resp_get, err_get := request.Get(baseurl, apipath_get_info)
	if err_get != nil {
		log.Println(err_get)
	}
	resp_get.RespPrint()
	log.Println("wait 30s......")
	time.Sleep(30 * time.Second)

	// delete policy
	// set baseurl and api path
	log.Printf("Delete Policy %s", policy.Policy_id)
	apipath_delete := apipath + "/" + policy.Policy_id
	resp_delete, err_delete := request.Delete(baseurl, apipath_delete)
	if err_delete != nil {
		log.Println(err_delete)
	}
	resp_delete.RespPrint()

	// health check
	for {
		resp_health, err_health := request.Get(baseurl, "/a1-policy/v2/status")
		if err_health != nil {
			log.Println(err_health)
		}
		log.Println(resp_health)
		time.Sleep(5 * time.Second) 
	}

}
