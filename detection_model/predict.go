package detection_model

import (
	"bytes"
	"fmt"
	"log"
	"net/http"
	"encoding/json"
	"strconv"
	// "reflect"
)

type Prediction struct {
		Prediction string `json:"prediction"`
}

func Predict(jsonData []byte) int {
	apiURL := "http://localhost:5000/predict"

	response, err := http.Post(apiURL, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatal("HTTP POST request failed:", err)
	}
	defer response.Body.Close()
	// print(response.Body)

	var prediction Prediction
	err = json.NewDecoder(response.Body).Decode(&prediction) // Decode the JSON response directly into the 'prediction' struct
	if err != nil {
		fmt.Println("Failed to decode response JSON:", err)
		return -1
	}
	temp, _ :=  strconv.Atoi(prediction.Prediction)
	// fmt.Println(reflect.TypeOf(prediction.Prediction))
	return temp
}