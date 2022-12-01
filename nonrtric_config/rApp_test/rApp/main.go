package main

import (
	"net/http"
	"fmt"
)

func main() {
	http.HandleFunc("/test", handler)
	http.ListenAndServe(":8081", nil)
	fmt.Println("listening 8081 port...")
}

func handler(w http.ResponseWriter, r *http.Request) {
	message := "Request URL Path is " + r.URL.Path
	w.Write([]byte(message))
}
