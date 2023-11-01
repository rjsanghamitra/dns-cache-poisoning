package prediction

import (
	"bytes"
	"io"
	"log"
	"net/http"
	"strconv"
)

func Predict() int {
	apiURL := "http://localhost:5000/predict" // ml model for detection of the safety of the site is predicted here

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
		log.Fatal("HTTP POST request failed:", err)
	}
	defer response.Body.Close()

	responseBody, err := io.ReadAll(response.Body)
	if err != nil {
		log.Fatal("Failed to read response body:", err)
		return -1
	}

	predictedValue, err := strconv.Atoi(string((string(responseBody))[9]))
	if err != nil {
		log.Fatal("Failed to convert response to integer:", err)
		return -1
	}
	return predictedValue
}
