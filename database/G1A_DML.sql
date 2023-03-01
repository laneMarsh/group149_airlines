-- -------------parts---------------
-- Create
INSERT INTO parts (name, capacity) 
VALUES (:part_number_input, :name_input, :description_input);

-- Read
SELECT * 
FROM parts;

-- Update
UPDATE parts
SET name = :name_input, capacity = :capacityInput, description = :description_input
WHERE part_number = :part_number_input;

-- Delete
DELETE FROM parts WHERE part_number = :part_number_input;


-- -------------aircraft---------------
-- Create
INSERT INTO aircraft (id_aircraft, model) 
VALUES (:id_aircraft_input, :model_input);

-- Read
SELECT * 
FROM aircraft;

-- Update
UPDATE aircraft
SET model = :model_input
WHERE id_aircraft = :id_aircraft_input;

-- Delete
DELETE FROM aircraft WHERE aircraft_id = :aircraft_id_input;


-- -------------repairs---------------
-- Create
INSERT INTO repairs (recieved, id_removal, supplier) 
VALUES (:recieved_input, :id_removal_dropDown, :supplier_input);

-- Read
SELECT repairs.id_repair, repairs.recieved, repairs.completed, removals.id_removal, repairs.supplier, repairs.price
FROM repairs
INNER JOIN removals ON repairs.id_removal = removals.id_removal
ORDER BY recieved DESC;

-- Update
UPDATE repairs
SET recieved = :recieved_input, completed = :completed_input, id_removal = :id_removal_dropDown, supplier = :supplier_input, price = :price_input
WHERE id_repair = :id_repair_input;

-- Delete
DELETE FROM repairs WHERE id_repair = :id_repair_input;


-- -------------removals---------------
-- Create
INSERT INTO removals (removal_date, id_aircraft, removed_part) 
VALUES (:removal_date_input, :id_aircraft_dropDown, :removed_part_dropDown);

-- Read
SELECT * 
FROM removals
INNER JOIN aircraft ON removals.id_aircraft = aircraft.id_aircraft
INNER JOIN parts AS parts1 ON removals.removed_part = parts1.part_number
INNER JOIN parts AS parts2 ON removals.installed_part = parts2.part_number
ORDER BY removal_date DESC;

-- Update
UPDATE removals
SET removal_date = :removal_date_input, replacement_date = :replacement_date_input, id_aircraft = :id_aircraft_dropDown, removed_part = :removed_part_dropDown, installed_part = :installed_part_dropDown
WHERE id_removal = :id_removal_input;

-- Delete
DELETE FROM Ports WHERE id_removal = :id_removal_input;


-- -------------inventory_locations---------------
-- Create
INSERT INTO inventory_locations (serial_number, location, part_number) 
VALUES (:serial_number_input, :location_input, :part_number_dropDown);

-- Read
SELECT inventory.id_inventory, inventory.serial_number, inventory.location, parts.part_number
FROM inventory_locations AS inventory
INNER JOIN parts ON inventory.part_number = parts.part_number;

-- Update
UPDATE inventory_locations
SET serial_number = :serial_number_input, location = :location_input, part_number = :part_number_dropDown
WHERE id_inventory = :id_inventory_input;

-- Delete
DELETE FROM inventory_locations WHERE id_inventory = :id_inventory_input;


-- -------------aircraft_parts---------------
-- Create
INSERT INTO aircraft_parts (id_aircraft, part_number) 
VALUES (:id_aircraft_dropDown, :part_number_dropDown);

-- Read
SELECT aircraft.aircraft_id AS id_aircraft, parts.part_number AS part_number
FROM aircraft_parts
INNER JOIN aircraft ON aircraft_parts.id_aircraft = aircraft.id_aircraft
INNER JOIN parts ON aircraft_parts.part_number = parts.part_number;

SELECT part_number.ac_parts, name.parts, description.parts
FROM aircraft_parts AS ac_parts
INNER JOIN parts ON ac_parts.part_number = parts.part_number
WHERE ac_parts.id_aircraft = "id_aircraft";

-- Delete
DELETE FROM aircraft_parts WHERE id_aircraft = :id_aircraft_dropDown AND part_number = :part_number_dropDown;
