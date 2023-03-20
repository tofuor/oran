# rApp-policy

## Overview

Package rApp-policy.

包含Get, Put, Delete Policy 功能。

```go
resp, err := request.Get(baseurl, apipath_get_info)
...
resp, err := request.Put(baseurl, apipath, policy)
...
resp, err := request.Delete(baseurl, apipath_delete)
```

部屬跟執行，需在Non-RT-RIC中啟動。
```
./build_rapp.sh
```

## Index

## Docker Build and Run

```go
docker build -t="rapp-policy:1.0.0" .
docker run --rm -d --network=nonrtric-docker-net --name rapp-policy rapp-policy:1.0.0
```

## Example

```go
package main

import (
	"httpclient/pkg/request"
	"log"
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
}

func main() {
	// create policy
	// set baseurl and api path
	baseurl := "http://:"
	apipath := "/a1-policy/v2/policies"

	policy := Policy{}
	policy.Ric_id = "ric2"
	policy.Policy_id = "" // UUID
	policy.Service_id = "controlpanel"
	policy.Policytype_id = "1"
	policy.Policy_data = make(map[string]any)
	policy.Transient = false

	// create policy
	log.Println("Create Policy")
	request := request.Request{}
	resp_create, err_create := request.Put(baseurl, apipath, policy)
	if err_create != nil {
		log.Println(err_create)
	}

	resp_create.RespPrint()

	// get policy information
	apipath_get_info := apipath + "/" + policy.Policy_id
	resp_get, err_get := request.Get(baseurl, apipath_get_info)
	if err_get != nil {
		log.Println(err_get)
	}
	resp_get.RespPrint()
}
```

## ****Variables****

```go
var(
		//set api ip and path
		baseurl := "IP:Port" 
		apipath := "/a1-policy/v2/policies"
)
```

```go
var(
		// policy create Policy struct
		policy   := &Policy{}
		// request is the default Request and is used by Get, Head, and Put.
		request  := &Request{}
		// response is the default Response and is used by Print response data
		response := &Response{}
)
```

## type Policy

```go
type Policy struct {
	// ric_id* string
	// identity of the target Near-RT RIC
	Ric_id                  string         `json:"ric_id"`
	
	// policy_id* string
	// identity of the policy
	Policy_id               string         `json:"policy_id"`
	
	// service_id* string
	// the identity of the service owning the policy
	Service_id              string         `json:"service_id"`

	// policytype_id*	string
	// identity of the policy type
	Policytype_id           string         `json:"policytype_id"`

	// status_notification_uri	string
	// Callback URI for policy status updates
	Status_notification_uri string         `json:"status_notification_uri"`
	
	Policy_data             map[string]any `json:"policy_data"`

	// transient	boolean
	// if true, the policy is deleted at RIC restart. 
	// If false, its value is maintained by this service until explicitly deleted. 
	// Default false.
	Transient               bool           `json:"transient"`
}
```

```
Example Value
{
  "ric_id": "string",
  "policy_id": "string",
  "transient": true,
  "service_id": "string",
  "policy_data": {},
  "status_notification_uri": "string",
  "policytype_id": "string"
}
```

## type Request

```go
type Request struct {
	baseurl string
	apipath string
	url     string
	method  string // get, put, delete
}
```

### func (r *Request) setBaseUrl

```go
func (r *Request) setBaseUrl(baseurl string) {
	r.baseurl = baseurl
}
```

### func (r *Request) setApiPath

```go
func (r *Request) setApiPath(path string) {
	r.apipath = path
}
```

### func (r *Request) buildUrl

```go
func (r *Request) buildUrl(baseurl string, apipath string) {
	r.setBaseUrl(baseurl)
	r.setApiPath(apipath)
	r.url = r.baseurl + r.apipath
}
```

### func (r *Request) buildBody

```go
// return payload
func (r *Request) buildBody(v any) (io.Reader, error) {
	if r.method == "GET" || r.method == "DELETE" {
		return nil, nil
	}

	body, err := json.Marshal(v)
	if err != nil {
		return nil, err
	}
	log.Println("json body", string(body))

	return bytes.NewBuffer(body), nil
}
```

### func (r *Request) request

```go
// return response, if err exist return err
func (r *Request) request(method, url string, v any) (*response.Response, error) {
	response := &response.Response{}
	body, err := r.buildBody(v)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest(method, url, body)
	if err != nil {
		return nil, err
	}
	req.Header.Add("Content-Type", "application/json")
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()
	sitemap, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	response.Body = sitemap
	return response, nil
}
```

### func (r *Request) Get

```go
// retrun response or error
// response 是根據api的不同取得不同資訊
func (r *Request) Get(baseurl string, apipath string) (*response.Response, error) {
	r.buildUrl(baseurl, apipath)
	r.method = "GET"
	resp, err := r.request(http.MethodGet, r.url, nil)
	if err != nil {
		return nil, err
	}
	return resp, nil
}
```

### func (r *Request) Put

```go
// retrun response or error
// response is success message or fail message
func (r *Request) Put(baseurl string, apipath string, v any) (*response.Response, error) {
	r.buildUrl(baseurl, apipath)
	r.method = "PUT"
	resp, err := r.request(http.MethodPut, r.url, v)
	if err != nil {
		return nil, err
	}
	return resp, nil
}
```

### func (r *Request) Delete

```go
// retrun response or error
func (r *Request) Delete(baseurl string, apipath string) (*response.Response, error) {
	r.buildUrl(baseurl, apipath)
	r.method = "DELETE"
	resp, err := r.request(http.MethodDelete, r.url, nil)
	if err != nil {
		return nil, err
	}
	return resp, nil
}
```

## type Response

```go
type Response struct {
	Body []byte
}
```

### func (r *Response) RespPrint()

```go
func (r *Response) RespPrint() {
	log.Println(string(r.Body))
}
```
