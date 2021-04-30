CREATE TABLE "Patients" (
	"id"	INTEGER NOT NULL,
	"firstname"	TEXT NOT NULL,
	"lastname"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"date_"	NUMERIC NOT NULL,
	"address"	BLOB NOT NULL,
	"healthcardno"	INTEGER NOT NULL,
	"p1"	INTEGER NOT NULL,
	"p2"	INTEGER NOT NULL,
	"p3"	INTEGER NOT NULL,
	"p4"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "Providers" (
	"id"	INTEGER NOT NULL,
	"firstname"	TEXT NOT NULL,
	"lastname"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "Users" (
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL,
	"email_address"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS Measurements
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    systolic INT NOT NULL,
    diastolic INT NOT NULL,
    pulse INT NOT NULL,
    time_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    patient_id INT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patients(id)
);