package response

import "log"

type Response struct {
	Body []byte
}

func (r *Response) RespPrint() {
	log.Println(string(r.Body))
}
