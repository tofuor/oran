package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/hello", HelloHandler)

	http.ListenAndServe(":8080", nil)
}

func HelloHandler(rw http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("name")
	content := fmt.Sprintf("hello, %s", name)
	fmt.Fprint(rw, content)
}
