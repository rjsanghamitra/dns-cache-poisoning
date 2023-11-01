package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"

	block "github.com/dns-spoofing/mitigation/blocker"
	"github.com/dns-spoofing/resolver"
	"github.com/joho/godotenv"
	"github.com/miekg/dns"
)

// struct to store ip details
type IPDetails struct {
	IP      string `json:"ip"`
	Country string `json:"country_name"`
}

// function to get location from ip address
func LocationFromIP(ip string) string {
	var envs map[string]string
	envs, err := godotenv.Read(".env")

	if err != nil {
		log.Fatal(err)
	}

	resp, err := http.Get("https://ipinfo.io/" + ip + "?access_key=" + envs["API_KEY"])
	if err != nil {
		log.Fatal(err)
	}

	var ipdetails IPDetails
	json.NewDecoder(resp.Body).Decode(&ipdetails)

	fmt.Println(ipdetails.Country)
	defer resp.Body.Close()
	return ipdetails.Country
}

type dnsHandler struct{}

func (h *dnsHandler) ServeDNS(w dns.ResponseWriter, r *dns.Msg) { // arg1 is an interface that used by a dns handler to construct a dns response. arg2 contains the layout of a dns message
	msg := new(dns.Msg)
	msg.SetReply(r)
	msg.Authoritative = true // this means that our server is authoritative
	resolver.NewCache.Flush()

	for _, question := range r.Question {

		fmt.Println("Received Query: ", question.Name)
		if resp, found := resolver.NewCache.Get(question.Name); found { // if record is present in cache, then return it
			rr, err := dns.NewRR(fmt.Sprint(resp))
			if err != nil {
				fmt.Println(err.Error())
			}
			msg.Answer = append(msg.Answer, rr)
		} else { // else resolve it
			resp := resolver.Resolve(question.Name, question.Qtype)

			// retrieving ip address before checking if it is fake or not
			// url, ip, location, url len, tld, record type
			var ip, location, tld, record_type string
			var url_len int
			var l []string
			if resp != nil {
				l = strings.Fields(resp[0].String())
				ip = l[len(l)-1]
				url := l[0]
				// location = LocationFromIP(ip)
				url_len = len(url)
				a := strings.Split(url, ".")
				tld = "." + a[len(a)-2]
				record_type = l[3]
				fmt.Println(tld)
				println(location, url_len, record_type)
				row := block.Db.QueryRow("SELECT * FROM blocked-addresses WHERE address = ", ip)
				var temp string
				row.Scan(&temp)
				if temp != "" { // if temp is not empty, it means the ip address is blocked. return for now.
					return
				} else { // else check if the ip address is authentic or fake based on the model
					block.CheckAndBlockIP(block.Db, ip)
				}
				resolver.NewCache.Set(question.Name, resp[0], 5*time.Minute)
				msg.Answer = append(msg.Answer, resp...)
			}
		}
		w.WriteMsg(msg) // this method writes a reply back to the client
	}
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
	defer block.Db.Close()
}
