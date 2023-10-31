package main

import (
	"fmt"
	"time"

	"github.com/dns-spoofing/resolver"
	"github.com/miekg/dns"
)

type dnsHandler struct{}

func (h *dnsHandler) ServeDNS(w dns.ResponseWriter, r *dns.Msg) { // arg1 is an interface that used by a dns handler to construct a dns response. arg2 contains the layout of a dns message
	msg := new(dns.Msg)
	msg.SetReply(r)
	msg.Authoritative = true // this means that our server is authoritative

	for _, question := range r.Question {
		fmt.Println("Received Query: ", question.Name)
		if resp, found := resolver.NewCache.Get(question.Name); found {
			rr, err := dns.NewRR(fmt.Sprint(resp))
			if err != nil {
				fmt.Println(err.Error())
			}
			msg.Answer = append(msg.Answer, rr)
			continue
		} else {
			resp := resolver.Resolve(question.Name, question.Qtype)
			resolver.NewCache.Set(question.Name, resp, 5*time.Minute)
			msg.Answer = append(msg.Answer, resp...)
		}
	}
	w.WriteMsg(msg) // this method writes a reply back to the client

}

func main() {
	handler := new(dnsHandler)
	server := &dns.Server{
		Addr:      ":53",
		Net:       "udp",
		Handler:   handler,
		ReusePort: true,
	}
	err := server.ListenAndServe()
	if err != nil {
		fmt.Println(err.Error())
	}
}
