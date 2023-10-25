package main

import (
	"fmt"
	"time"

	"github.com/dns-spoofing/resolver"
	"github.com/miekg/dns"
)

type dnsHandler struct{}

func (h *dnsHandler) ServeDNS(w dns.ResponseWriter, r *dns.Msg) {
	msg := new(dns.Msg)
	msg.SetReply(r)

	for _, question := range r.Question {
		fake, err := dns.NewRR(fmt.Sprintf("%s IN %s 127.0.0.1", question.Name, dns.TypeToString[question.Qtype]))
		if err != nil {
			fmt.Println(err)
		}
		msg.Answer = append(msg.Answer, fake)
		resolver.NewCache.Set(question.Name, fake, 5*time.Minute)
	}
	w.WriteMsg(msg)
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
