package database

import (
	"database/sql"
	"log"

	_ "github.com/mattn/go-sqlite3"
)

func CheckErr(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func CreateTable(db sql.DB, name string) {
	com := "CREATE TABLE IF NOT EXISTS " + name + " (\"address\" TEXT)"
	stmt, err := db.Prepare(com)
	CheckErr(err)
	stmt.Exec()
}

func InsertIntoTable(db *sql.DB, name string, addr string) {
	com := "INSERT INTO " + name + "(addr) VALUES(?)"
	stmt, err := db.Prepare(com)
	CheckErr(err)
	stmt.Exec(addr)
}
