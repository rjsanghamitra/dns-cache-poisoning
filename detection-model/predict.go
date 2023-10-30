package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"strconv"
)

func main() {
    apiURL := "http://localhost:5000/predict"  

	// jsonData := []byte(`{"url": "http://members.tripod.com/russiastation/", 
    //         "url_len": 40, 
    //         "ip_add": "42.77.221.155", 
    //         "geo_loc": "Taiwan",
    //         "tld": "com",
    //         "who_is": "complete",
    //         "https": "yes",
    //         "js_len": 58, 
    //         "js_obf_len": 0}`)

	jsonData := []byte(`{"url": "http://www.ff-b2b.de/", 
            "url_len": 21, 
            "ip_add": "147.22.38.45", 
            "geo_loc": "United States",
            "tld": "de",
            "who_is": "incomplete",
            "https": "no",
            "js_len": 720, 
            "js_obf_len": 532.8}`)

    response, err := http.Post(apiURL, "application/json", bytes.NewBuffer(jsonData))
    if err != nil {
        fmt.Println("HTTP POST request failed:", err)
        return
    }
    defer response.Body.Close()

	fmt.Println(response.Body)

    responseBody, err := io.ReadAll(response.Body)
	if err != nil {
        fmt.Println("Failed to read response body:", err)
        return
    }
	
	predictedValue, err := strconv.Atoi(string((string(responseBody))[9]))
    if err != nil {
        fmt.Println("Failed to convert response to integer:", err)
        return
    }
    fmt.Println("Prediction: ", predictedValue)
}
