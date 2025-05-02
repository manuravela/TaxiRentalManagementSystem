CREATE TABLE Manager (
    ssn VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (ssn)
);

CREATE TABLE Client (
    email VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (email)
);

CREATE TABLE Car (
    car_id INT GENERATED ALWAYS AS IDENTITY,
    brand VARCHAR(255) NOT NULL,
    PRIMARY KEY (car_id)
);

CREATE TABLE Address (
    road_name VARCHAR(255) NOT NULL,
    number VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    PRIMARY KEY (road_name, number, city)
);

CREATE TABLE Model (
    model_id INT GENERATED ALWAYS AS IDENTITY,
    color VARCHAR(255) NOT NULL,
    construction_year INT NOT NULL,
    transmission_type VARCHAR(255) CHECK (transmission_type = 'manual' OR transmission_type = 'automatic'),
    car_id INT NOT NULL,
    PRIMARY KEY (model_id, car_id),
    FOREIGN KEY (car_id) REFERENCES Car(car_id) ON DELETE CASCADE
);

CREATE TABLE Driver (
    name VARCHAR(255),
    address_road_name VARCHAR(255) NOT NULL,
    address_number VARCHAR(255) NOT NULL,
    address_city VARCHAR(255) NOT NULL,
    PRIMARY KEY (name),
    FOREIGN KEY (address_road_name, address_number, address_city) REFERENCES Address(road_name, number, city)
);

CREATE TABLE Rent (
    rent_id INT GENERATED ALWAYS AS IDENTITY,
    date DATE NOT NULL,
    client_email VARCHAR(255),
    model_id INT NOT NULL,
    car_id INT NOT NULL,
    driver_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (rent_id),
    FOREIGN KEY (client_email) REFERENCES Client (email),
    FOREIGN KEY (model_id, car_id) REFERENCES Model(model_id, car_id),
    FOREIGN KEY (driver_name) REFERENCES Driver (name)
);

CREATE TABLE CreditCard (
    credit_card_number VARCHAR(255),
    client_email VARCHAR(255) NOT NULL,
    address_road_name VARCHAR(255) NOT NULL,
    address_number VARCHAR(255) NOT NULL,
    address_city VARCHAR(255) NOT NULL,
    PRIMARY KEY (credit_card_number),
    FOREIGN KEY (client_email) REFERENCES Client(email),
    FOREIGN KEY (address_road_name, address_number, address_city) REFERENCES Address(road_name, number, city)
);

CREATE TABLE Review (
    review_id INT GENERATED ALWAYS AS IDENTITY,
    message TEXT,
    rating INT NOT NULL CHECK (rating BETWEEN 0 AND 5),
    driver_name VARCHAR(255) NOT NULL,
    client_email VARCHAR(255) NOT NULL,
    PRIMARY KEY (review_id, driver_name),
    FOREIGN KEY (driver_name) REFERENCES Driver(name) ON DELETE CASCADE,
    FOREIGN KEY (client_email) REFERENCES Client(email)
);

CREATE TABLE ClientResidesAddress (
    client_email VARCHAR(255) NOT NULL,
    address_road_name VARCHAR(255) NOT NULL,
    address_number VARCHAR(255) NOT NULL,
    address_city VARCHAR(255) NOT NULL,
    PRIMARY KEY (client_email, address_road_name, address_number, address_city),
    FOREIGN KEY (client_email) REFERENCES Client(email),
    FOREIGN KEY (address_road_name, address_number, address_city) REFERENCES Address(road_name, number, city)
);

CREATE TABLE DriverDrivesModel (
    driver_name VARCHAR(255) NOT NULL,
    model_id INT NOT NULL,
    car_id INT NOT NULL,
    PRIMARY KEY (driver_name, model_id, car_id),
    FOREIGN KEY (driver_name) REFERENCES Driver(name),
    FOREIGN KEY (model_id, car_id) REFERENCES Model(model_id, car_id)
);
