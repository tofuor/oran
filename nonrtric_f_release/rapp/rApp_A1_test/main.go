package main

import (
	"bytes"
	"crypto/tls"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"rAppPolicy_combine/pkg/request"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/goccy/go-json"
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

var policy_test = Policy{
	Ric_id:        "ric2",
	Policy_id:     "422522d3-2b60-44b3-b7db-cdef6fb4df22", // UUID
	Service_id:    "control-panel",
	Policytype_id: "1",
	Policy_data:   make(map[string]any),
	Transient:     false,
}

type ProducerRegistrationInfo struct {
	InfoProducerSupervisionCallbackUrl string   `json:"info_producer_supervision_callback_url"`
	SupportedInfoTypes                 []string `json:"supported_info_types"`
	InfoJobCallbackUrl                 string   `json:"info_job_callback_url"`
}

var Producer_test = ProducerRegistrationInfo{
	InfoProducerSupervisionCallbackUrl: "https://rapp-policy:6969/health_check",
	SupportedInfoTypes:                 []string{"A1_EI_test_Messages"},
	InfoJobCallbackUrl:                 "https://rapp-policy:6969/info_job",
}

type ProducerType struct {
	Identity   string `json:"id"`
	testUrl    string `json:"test_A1-EI_url"`
	TypeSchema interface{}
}

var producer_type_test = ProducerType{
	Identity:   "A1_EI_test_Messages",
	testUrl:    "test-A1-EI",
	TypeSchema: make(map[string]any),
}

type info_job_Payload struct {
	InfoJobIdentity  string                 `json:"info_job_identity"`
	InfoTypeIdentity string                 `json:"info_type_identity"`
	InfoJobData      map[string]interface{} `json:"info_job_data"`
	TargetURI        string                 `json:"target_uri"`
	Owner            string                 `json:"owner"`
	LastUpdated      time.Time              `json:"last_updated"`
}

func main() {
	// create policy
	// set baseurl and api path
	const gatewayUrl = "http://192.168.122.35:9090"
	const icsUrl = "https://information-coordinator-service:8434"
	const policyPath = "/a1-policy/v2/policies"
	const registerTypePath = "/data-producer/v1/info-types/"
	const registerProducerPath = "/data-producer/v1/info-producers/"
	const producer_port = 6969
	const ProducerID = "A1_EI_test_Producer"

	/**********A1 policy function**********/
	// create policy
	// create_policy(policy_test, gatewayUrl, policyPath)

	// // get policy information
	// get_policy(policy_test, gatewayUrl, policyPath)

	// // delete policy
	// delete_policy(policy_test, gatewayUrl, policyPath)

	// // health check
	// health_check(gatewayUrl)

	/**********A1-EI message function**********/
	// registry type
	type_registry(producer_type_test, icsUrl, registerTypePath)

	// registry producer
	producer_registry(Producer_test, icsUrl, registerProducerPath, producer_port, ProducerID)

	// inform data
	//request_data(icsUrl)

	// send data
	//send_data(icsUrl)

	keepProducerAlive()

}

/**********A1-EI message function**********/
func type_registry(producer_type ProducerType, icsurl string, apipath string) {
	fmt.Println("Start Registry type")
	typeDefsByte, err := os.ReadFile(filepath.Join("configs", "typeSchemaDmaap.json"))
	if err != nil {
		log.Fatalf("File reading error: %v", err)
	}

	body := fmt.Sprintf(`{"info_job_data_schema": %v}`, string(typeDefsByte))
	// 創建帶有 tls 證書的 HTTP 客戶端
	tls_client := TLS_client()
	path := icsurl + apipath + url.PathEscape(producer_type.Identity)
	// 創建 PUT 請求
	req, err := http.NewRequest("PUT", path, nil)
	req.Header.Set("Content-Type", "application/json")
	byte_body := []byte(body)
	req.Body = ioutil.NopCloser(bytes.NewReader(byte_body))
	if err != nil {
		fmt.Println("Failed to create PUT request:", err)
		return
	}

	resp, err := tls_client.Do(req)
	if err != nil {
		log.Println(err)
	}
	payload, _ := ioutil.ReadAll(resp.Body)

	fmt.Println(string(payload))
}

func producer_registry(Producer ProducerRegistrationInfo, icsurl string, apipath string, port int, Producerid string) {
	fmt.Println("Start Registry producer")
	go CallbackServer(port)
	// 創建帶有 tls 證書的 HTTP 客戶端
	tls_client := TLS_client()
	path := icsurl + apipath + url.PathEscape(Producerid)
	// 創建 PUT 請求
	req, err := http.NewRequest("PUT", path, nil)
	req.Header.Set("Content-Type", "application/json")
	// 製作body
	byte_body, _ := json.Marshal(Producer)
	req.Body = ioutil.NopCloser(bytes.NewReader(byte_body))
	if err != nil {
		fmt.Println("Failed to create PUT request:", err)
		return
	}
	// 發送messages
	resp, err := tls_client.Do(req)
	if err != nil {
		log.Println(err)
	}
	payload, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(payload))

}

func TLS_client() *http.Client {
	cert, err := tls.LoadX509KeyPair("security/producer.crt", "security/producer.key")
	if err != nil {
		fmt.Println("Failed to load TLS certificate and key:", err)
		return nil
	}

	config := &tls.Config{
		Certificates:       []tls.Certificate{cert},
		InsecureSkipVerify: true,
	}

	// 創建帶有 tls 證書的 HTTP 客戶端
	client := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: config,
		},
	}
	return client
}

func CallbackServer(port int) {

	fmt.Print("Starting callback server at port")
	cert, err := tls.LoadX509KeyPair("security/producer.crt", "security/producer.key")
	if err != nil {
		panic(err)
	}

	// gin router
	r := gin.Default()
	r.GET("/health_check", healthCheckHandler)
	r.POST("/info_job", infoJobHandler)
	r.DELETE("/info_job/job2", stopDeliveryMessageHandler)

	// 設定Server參數
	addr := ":" + strconv.Itoa(port)
	server := &http.Server{
		Addr: addr,
		TLSConfig: &tls.Config{
			Certificates: []tls.Certificate{cert},
		},
		Handler: r,
	}

	// 啟動Server
	if err := server.ListenAndServeTLS("", ""); err != nil {
		panic(err)
	}

}

func healthCheckHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"message": "This is a health check",
	})
}

func infoJobHandler(c *gin.Context) {
	var payload info_job_Payload
	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"message": "Failed to read payload",
		})
		return
	}

	message := map[string]string{
		"job":     "2",
		"payload": "mitlab sugar daddy",
	}
	messageJson, _ := json.Marshal(message)

	if _, err := http.Post(payload.TargetURI, "application/json", bytes.NewBuffer(messageJson)); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "start delivery message",
	})
}

func stopDeliveryMessageHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"message": "stop delivery message",
	})
}

/***********Other function*************/
func keepProducerAlive() {
	forever := make(chan int)
	<-forever
}

/**********A1 policy function**********/
func health_check(gatewayUrl string) {
	request := request.Request{}
	resp, err := request.Get(gatewayUrl, "/a1-policy/v2/status")
	if err != nil {
		log.Println("health check error")
		log.Println(err)
	} else {
		log.Println(resp)
	}
}

func delete_policy(policy Policy, baseurl string, apipath string) {
	request := request.Request{}
	log.Printf("Delete Policy %s", policy.Policy_id)
	path := apipath + "/" + policy.Policy_id
	resp, err := request.Delete(baseurl, path)
	if err != nil {
		log.Println(err)
	}
	resp.RespPrint()
}

func get_policy(policy Policy, baseurl string, apipath string) {
	request := request.Request{}
	path := apipath + "/" + policy.Policy_id
	resp, err := request.Get(baseurl, path)
	if err != nil {
		log.Println(err)
	}
	resp.RespPrint()
}

func create_policy(policy Policy, baseurl string, apipath string) {
	log.Printf("Create Policy %s", policy.Policy_id)
	request := request.Request{}
	resp, err := request.Put(baseurl, apipath, policy)
	if err != nil {
		log.Println(err)
	}
	resp.RespPrint()
}
