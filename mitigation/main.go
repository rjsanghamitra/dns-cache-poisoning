package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"

	block "github.com/dns-spoofing/mitigation/blocker"
	"github.com/dns-spoofing/mitigation/database"
	"github.com/dns-spoofing/resolver"
	"github.com/miekg/dns"
)

type WebPageData struct {
	URL    string `json:"url"`
	URLLen int    `json:"url_len"`
	IPAddr string `json:"ip_add"`
	TLD    string `json:"tld"`
	HTTPS  string `json:"https"`
}

func isHTTPS(url string) string {
	resp, err := http.Get(url)

	if err != nil {
		log.Fatal(err)
	}

	returnedURL := resp.Request.URL.String()

	if strings.HasPrefix(returnedURL, "https") {
		return "yes"
	} else {
		return "no"
	}
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
			var ip, tld string
			var url_len int
			var l []string
			if resp != nil {

				// get details
				l = strings.Fields(resp[0].String())
				ip = l[len(l)-1]
				url := l[0]
				// location = LocationFromIP(ip)
				url_len = len(url)
				a := strings.Split(url, ".")
				tld = "." + a[len(a)-2]

				jsonData := WebPageData{
					URL:    url,
					URLLen: url_len,
					IPAddr: ip,
					TLD:    tld,
					// HTTPS:  isHTTPS("https://" + url),
					HTTPS: "yes",
				}

				reqData, err := json.Marshal(jsonData)
				database.CheckErr(err)

				// check if the ip address is present in the database(blocked addresses)
				Db, err := sql.Open("sqlite3", "./database/dns.db")
				defer Db.Close()
				database.CheckErr(err)
				row := Db.QueryRow("SELECT * FROM blocked WHERE address = ", ip)
				var temp string
				row.Scan(&temp)
				if temp != "" { // if temp is not empty, it means the ip address is blocked. return for now.
					return
				} else { // else check if the ip address is authentic or fake based on the model
					block.CheckAndBlockIP(Db, ip, []byte(reqData))
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
}
