package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"

	detection_model "github.com/dns-spoofing/detection-model"
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

	resp, err := http.Get("http://api.ipstack.com/" + ip + "?access_key=" + envs["API_KEY"])
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

	for _, question := range r.Question {
		fmt.Println(dns.TypeToString[question.Qtype])
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

			// retrieving ip address before checking if it is fake or not
			// url, ip, location, url len, tld, record type
			var ip string
			l := strings.Fields((*resp).String())
			ip = l[len(l)-1]
			fmt.Println(l, ip)
			url := l[0]
			// location := LocationFromIP(ip)	// this is the api. leads to errors
			location := "temp"
			url_len := len(url)
			a := strings.Split(url, ".")
			tld := a[len(a)-1]
			
			jsonData := []byte(`{"url": "http://www.ff-b2b.de/", 
			        "url_len": 21, 
			        "ip_add": "147.22.38.45", 
			        "geo_loc": "United States",
			        "tld": "de",
			        "https": "no",}`)
			fmt.Println(detection_model.Predict(jsonData))
			
			record_type := l[3]
			fmt.Println(url, location, url_len, tld, record_type)
			row := block.Db.QueryRow("SELECT * FROM blocked-addresses WHERE address = ", ip)
			var temp string
			row.Scan(&temp)
			if temp != "" { // if temp is not empty, it means the ip address is blocked. return for now.
				return
			} else { // else check if the ip address is authentic or fake based on the model
				block.CheckAndBlockIP(block.Db, ip)
			}
			resolver.NewCache.Set(question.Name, resp, 5*time.Minute)
			msg.Answer = append(msg.Answer, (*resp))
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
	defer block.Db.Close()
}
