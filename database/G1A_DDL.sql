DROP TABLE repairs;
DROP TABLE removals;
DROP TABLE inventory_locations;
DROP TABLE aircraft_parts;
DROP TABLE aircraft;
DROP TABLE parts;

CREATE OR REPLACE TABLE parts (
	part_number varchar(45) NOT NULL,
    name varchar(45) NOT NULL,
    description varchar(45) NOT NULL,
    PRIMARY KEY(part_number)
);

CREATE OR REPLACE TABLE aircraft (
	id_aircraft varchar(45) NOT NULL,
    model varchar(45) NOT NULL,
    PRIMARY KEY(id_aircraft)
);

CREATE OR REPLACE TABLE aircraft_parts (
	id_aircraft varchar(45) NOT NULL,
    part_number varchar(45) NOT NULL,
    FOREIGN KEY(id_aircraft) REFERENCES aircraft(id_aircraft),
    FOREIGN KEY(part_number) REFERENCES parts(part_number)
);

CREATE OR REPLACE TABLE inventory_locations(
	id_inventory int NOT NULL AUTO_INCREMENT,
    serial_number varchar(45) NOT NULL,
    location varchar(45) NOT NULL,
    part_number varchar(45),
    PRIMARY KEY(id_inventory),
    FOREIGN KEY(part_number) REFERENCES parts(part_number)
);

CREATE OR REPLACE TABLE removals(
	id_removal int NOT NULL AUTO_INCREMENT,
    removal_date datetime NOT NULL,
    replacement_date datetime,
    id_aircraft varchar(45) NOT NULL,
    removed_part varchar(45) NOT NULL,
    installed_part varchar(45),
    PRIMARY KEY (id_removal),
    FOREIGN KEY(id_aircraft) REFERENCES aircraft(id_aircraft),
    FOREIGN KEY(removed_part) REFERENCES parts(part_number),
    FOREIGN KEY(installed_part) REFERENCES parts(part_number)
);

CREATE OR REPLACE TABLE repairs (
	id_repair int NOT NULL AUTO_INCREMENT,
    recieved datetime NOT NULL,
    completed datetime,
    id_removal int NOT NULL,
    supplier varchar(45) NOT NULL,
    price float(10,2),
    PRIMARY KEY(id_repair),
    FOREIGN KEY(id_removal) REFERENCES removals(id_removal)
);

INSERT INTO parts (
    part_number,
    name,
    description
)
VALUES 
(
    "123A4567-1",
    "Fuselage",
    "Boeing's single aisle, aerodynamic tube where the aircraft payload goes"
),
(
    "987A6543-1",
    "Left Wing",
    "Provides lift and attaches to the left side of a B737 fuselage"
),
(
    "987A6543-2",
    "Right Wing",
    "Provides lift and attaches to the right side of a B737 fuselage"
);

INSERT INTO aircraft (
    id_aircraft,
    model
)
VALUES 
(
    "G1A-01",
    "B737"
),
(
    "G1A-02",
    "B737"
),
(
    "G1A-03",
    "B737"
),
(
    "G1A-04",
    "B737"
),
(
    "G1A-05",
    "B737"
),
(
    "G1A-06",
    "B737"
),
(
    "G1A-51",
    "A320"
),
(
    "G1A-53",
    "A320"
);

INSERT INTO aircraft_parts (
    part_number,
    id_aircraft
)
VALUES
(
    "123A4567-1",
    "G1A-01"
),
(
    "987A6543-1",
    "G1A-01"
),
(
    "987A6543-2",
    "G1A-01"
);

INSERT INTO inventory_locations (
    serial_number,
    part_number,
    location
)
VALUES
(
    "abc123",
    "123A4567-1",
    "G1A-01"
),
(
    "abc123",
    "987A6543-1",
    "G1A-01"
),
(
    "abc123",
    "987A6543-2",
    "G1A-01"
),
(
    "abc124",
    "123A4567-1",
    "G1A-02"
),
(
    "abc125",
    "987A6543-1",
    "G1A-02"
),
(
    "abc126",
    "987A6543-2",
    "G1A-02"
);

INSERT INTO removals (
    removal_date,
    replacement_date,
    id_aircraft,
    removed_part,
    installed_part
)
VALUES
(
    "2023-02-01",
    "2018-02-02",
    "G1A-01",
    "987A6543-1",
    "987A6543-1"
),
(
    "2023-02-09",
    NULL,
    "G1A-02",
    "987A6543-2",
    NULL
);

INSERT INTO repairs (
    recieved,
    id_removal,
    supplier,
    price
)
VALUES
(
    "2023-02-02",
    NULL,
    "1",
    "Spirit Aerospace",
    "350.00"
),
(
    "2023-02-09",
    NULL,
    "2",
    "Spirit Aerospace",
    NULL
);

SELECT * FROM parts;
SELECT * FROM aircraft;
SELECT * FROM repairs;
SELECT * FROM removals;
SELECT * FROM inventory_locations;
SELECT * FROM aircraft_parts;
