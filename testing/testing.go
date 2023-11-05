package main

import (
	"encoding/json"
	"fmt"

	detection_model "github.com/dns-spoofing/detection-model"
)


type WebPageData struct {
    URL     string `json:"url"`
    URLLen  int    `json:"url_len"`
    IPAddr  string `json:"ip_add"`
    TLD     string `json:"tld"`
}

func main() {
    jsonData := WebPageData{
        URL:     "https://www.google.com/",
        URLLen:  len("http://www.google.com/"),
        IPAddr:  "142.250.66.14",
        TLD:     "com",
    }
    
	requestData, err := json.Marshal(jsonData)
    if err != nil {
        fmt.Println("JSON marshaling failed:", err)
        return
    }

    prediction := detection_model.Predict([]byte(requestData))
	fmt.Println(prediction)
}