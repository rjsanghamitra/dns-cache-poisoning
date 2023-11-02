package block

import (
	"database/sql"
	"os"

	detection_model "github.com/dns-spoofing/detection-model"
	"github.com/dns-spoofing/mitigation/database"
)

func CheckAndBlockIP(db *sql.DB, addr string, reqData []byte) {
	database.CreateTable(*db, "blocked")
	if res := detection_model.Predict(reqData); res == 0 {
		database.InsertIntoTable(db, "blocked", addr)
		os.Exit(1)
	}
}
