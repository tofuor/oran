package request

import (
	"bytes"
	"encoding/json"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"rAppPolicy/pkg/response"
)

type Request struct {
	baseurl string
	apipath string
	url     string
	method  string
}

func (r *Request) setBaseUrl(baseurl string) {
	r.baseurl = baseurl
}

func (r *Request) setApiPath(path string) {
	r.apipath = path
}

func (r *Request) buildUrl(baseurl string, apipath string) {
	r.setBaseUrl(baseurl)
	r.setApiPath(apipath)
	r.url = r.baseurl + r.apipath
}

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

func (r *Request) Get(baseurl string, apipath string) (*response.Response, error) {
	r.buildUrl(baseurl, apipath)
	r.method = "GET"
	resp, err := r.request(http.MethodGet, r.url, nil)
	if err != nil {
		return nil, err
	}
	return resp, nil
}

func (r *Request) Put(baseurl string, apipath string, v any) (*response.Response, error) {
	r.buildUrl(baseurl, apipath)
	r.method = "PUT"
	resp, err := r.request(http.MethodPut, r.url, v)
	if err != nil {
		return nil, err
	}
	return resp, nil
}

func (r *Request) Delete(baseurl string, apipath string) (*response.Response, error) {
	r.buildUrl(baseurl, apipath)
	r.method = "DELETE"
	resp, err := r.request(http.MethodDelete, r.url, nil)
	if err != nil {
		return nil, err
	}
	return resp, nil
}
