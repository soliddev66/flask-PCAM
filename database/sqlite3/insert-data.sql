INSERT INTO Users (email_address, username, password) VALUES
	('pmadziak@conestogac.on.ca','sjones','pwd1'),
	('peter.madziak@gmail.com','lsmith','pwd2'),
	('bjulius5513@conestogac.on.ca','precious','pbkdf2:sha256:150000$7Xa8c3RT$3ff3560884c15b6cc8dfb21bf66d70d0cf399dd5553e50e13273d3a7494bff19');


INSERT INTO Patients (firstname, lastname, name, email, date_, address, healthcardno, p1, p2, p3, p4) VALUES ('Anna', 'Jones', 'Anna Jones', 'anna@example.com', '02-14-1995', 'AAA', '123', -1, -1, -1, -1);
INSERT INTO Patients (firstname, lastname, name, email, date_, address, healthcardno, p1, p2, p3, p4) VALUES ('Allan', 'Smith', 'Allan Smith', 'allan@example.com', '02-14-1995', 'AAA', '124', -1, -1, -1, -1);
INSERT INTO Patients (firstname, lastname, name, email, date_, address, healthcardno, p1, p2, p3, p4) VALUES ('Alex', 'Smith', 'Alex Smith', 'alex@example.com', '02-14-1995', 'AAA', '125', -1, -1, -1, -1);
INSERT INTO Patients (firstname, lastname, name, email, date_, address, healthcardno, p1, p2, p3, p4) VALUES ('Allan', 'Smith', 'Allan Smith', 'allan@example.com', '02-14-1995', 'AAA', '124', -1, -1, -1, -1);
INSERT INTO Patients (firstname, lastname, name, email, date_, address, healthcardno, p1, p2, p3, p4) VALUES ('Andrea', 'Smith', 'Andrea Smith', 'andrea@example.com', '02-14-1995', 'AAA', '127', -1, -1, -1, -1);
INSERT INTO Patients (firstname, lastname, name, email, date_, address, healthcardno, p1, p2, p3, p4) VALUES ('Albie', 'Jones', 'Albie Jones', 'albie@example.com', '02-14-1995', 'AAA', '128', -1, -1, -1, -1);
INSERT INTO Patients (firstname, lastname, name, email, date_, address, healthcardno, p1, p2, p3, p4) VALUES ('Albie', 'Jones', 'Albie Jones', 'albie@example.com', '02-14-1995', 'AAA', '128', -1, -1, -1, -1);
INSERT INTO Patients (firstname, lastname, name, email, date_, address, healthcardno, p1, p2, p3, p4) VALUES ('Ahmed', 'Fahad', 'Ahmed Fahad', 'ahmed@example.com', '02-14-1995', 'AAA', '130', -1, -1, -1, -1);

INSERT INTO Measurements (systolic,diastolic,pulse,patient_id) VALUES (120,80,90,1);
INSERT INTO Measurements (systolic,diastolic,pulse,patient_id) VALUES (122,78,90,1);
