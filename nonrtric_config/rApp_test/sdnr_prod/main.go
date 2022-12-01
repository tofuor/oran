package main

import (
	"log"
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
	// 自訂數值型態的測量數據。
	cpuTemp = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cpu_temperature_celsius",
		Help: "CPU 目前的溫度。",
	})
	// 計數型態的測量數據，並帶有自訂標籤。
	hdFailures = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "hd_errors_total",
			Help: "硬碟發生錯誤的次數。",
		},
		[]string{"裝置"},
	)
)

func init() {
	// 測量數據必須註冊才會暴露給外界知道：
	prometheus.MustRegister(cpuTemp)
	prometheus.MustRegister(hdFailures)
}

func main() {
	// 配置測量數據的數值。
	cpuTemp.Set(65.3)
	hdFailures.With(prometheus.Labels{"裝置": "/dev/sda"}).Inc()

	// 我們會用 Prometheus 所提供的預設處理函式在 "/metrics" 路徑監控著。
	// 這會暴露我們的數據內容，所以 Prometheus 就能夠獲取這些數據。
	http.Handle("/metrics", promhttp.Handler())
	log.Fatal(http.ListenAndServe(":8080", nil))
}