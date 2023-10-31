package block

import (
	"database/sql"

	"github.com/dns-spoofing/mitigation/database"
)

var Db, err = sql.Open("sqlite3", "./dns.db")

func CheckAndBlockIP(db *sql.DB, addr string) {
	database.CheckErr(err)
	database.CreateTable(*Db, "blocked")
	if addr == "127.0.0.1" {
		database.InsertIntoTable(Db, "blocked", addr)
	}
}
