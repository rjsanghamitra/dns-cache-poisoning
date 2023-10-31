package resolver

import (
	"fmt"
	"time"

	"github.com/miekg/dns"
	"github.com/patrickmn/go-cache"
)

var NewCache cache.Cache = *cache.New(5*time.Minute, 10*time.Minute) // the expiration time and the time after expiration after which the item should be purged

func Resolve(domain string, qtype uint16) *dns.RR { // this function resolves a domain name
	m := new(dns.Msg)                      // Msg contains the layout of a new dns packet
	m.SetQuestion(dns.Fqdn(domain), qtype) // creates a question from the given domain name. Fqdn creates a fully qualified domain name from the given domain name.
	m.RecursionDesired = true              // recursively check other nameservers

	c := new(dns.Client)
	in, _, err := c.Exchange(m, "1.1.1.1:53") // the exchange function performs a sync query. it sends the message to the address(2nd parameter).
	if err != nil {
		fmt.Println(err)
		return nil
	}

	response := &in.Answer[0]
	return response
}
