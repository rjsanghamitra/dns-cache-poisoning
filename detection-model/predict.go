package detection_model

import (
	"bytes"
	"fmt"
	"log"
	"net/http"
	"encoding/json"
)

type Prediction struct {
		Prediction int `json:"prediction"`
}

func Predict(jsonData []byte) int {
	apiURL := "http://localhost:5000/predict"

	response, err := http.Post(apiURL, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatal("HTTP POST request failed:", err)
	}
	defer response.Body.Close()

	var prediction Prediction
	decoder := json.NewDecoder(response.Body)
    if err := decoder.Decode(&prediction); err != nil {
        fmt.Println("Failed to decode response JSON:", err)
        return -1
    }
	return prediction.Prediction
}