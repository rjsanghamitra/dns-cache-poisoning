package main

import (
	"encoding/json"
	"fmt"

	detection_model "github.com/dns-spoofing/detection-model"
)

type WebPageData struct {
	URL    string `json:"url"`
	URLLen int    `json:"url_len"`
	IPAddr string `json:"ip_add"`
	TLD    string `json:"tld"`
	HTTPS  string `json:"https"`
}

func main() {
	jsonData := WebPageData{
		URL:    "http://www.ff-b2b.de/",
		URLLen: 21,
		IPAddr: "147.22.38.45",
		TLD:    "de",
		HTTPS:  "no",
	}

	requestData, err := json.Marshal(jsonData)
	if err != nil {
		fmt.Println("JSON marshaling failed:", err)
		return
	}

	prediction := detection_model.Predict([]byte(requestData))
	fmt.Println(prediction)
}
