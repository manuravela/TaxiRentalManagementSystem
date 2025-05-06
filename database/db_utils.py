from .db import connection, cursor

def getDriver(name):
    sql = """
        SELECT * FROM Driver WHERE name = %s;
    """
    cursor.execute(sql, [name])
    data = cursor.fetchone()
    return {
        "name": data[0],
        "address_road_name": data[1],
        "address_number": data[2],
        "address_city": data[3]
    } if data else None

def getModelsDrivenBy(name):
    sql = """
        SELECT model_id, car_id
        FROM DriverDrivesModel
        WHERE driver_name = %s;
    """
    cursor.execute(sql, [name])
    data = cursor.fetchall()
    return [{
        "model_id": item[0],
        "car_id": item[1]
    } for item in data]

def updateDriverAddress(name, road, number, city):
    try:
        # Insert address if not exists
        try:
            sql = """
                INSERT INTO Address (road_name, number, city)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
            cursor.execute(sql, [road, number, city])
            connection.commit()
        except:
            connection.rollback()

        # Update driver's address
        sql = """
            UPDATE Driver
            SET address_road_name = %s, address_number = %s, address_city = %s
            WHERE name = %s;
        """
        cursor.execute(sql, [road, number, city, name])
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e

def declareModelForDriver(name, model_id, car_id):
    try:
        sql = """
            INSERT INTO DriverDrivesModel (driver_name, model_id, car_id)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """
        cursor.execute(sql, [name, model_id, car_id])
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e

def getManager(ssn):
    sql = """
        SELECT * FROM manager WHERE ssn = %s;
    """
    cursor.execute(sql, [ssn])
    data = cursor.fetchone()
    return {
        "ssn": data[0],
        "name": data[1],
        "email": data[2]
    } if data else None

def getAllCars():
    sql = """
        SELECT * FROM Car;
    """ 
    cursor.execute(sql)
    data = cursor.fetchall()
    return [{
        "car_id": item[0],
        "brand": item[1]
    } for item in data]

def getAllModels():
    sql = """
        SELECT * FROM Model;
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    return [{
        "model_id": item[0],
        "color": item[1],
        "construction_year": item[2],
        "transmission_type": item[3],
        "car_id": item[4]
    } for item in data]

def getAllDrivers():
    sql = """
        SELECT * FROM Driver;
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    return [{
        "name": item[0],
        "address_road_name": item[1],
        "address_number": item[2],
        "address_city": item[3]
    } for item in data]

def insertCar(brand):
    try:
        sql = """
            INSERT INTO Car (brand)
            VALUES (%s);
        """
        cursor.execute(sql, [brand])
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e

def removeCar(car_id):
    try:
        sql = """
            DELETE FROM Car
            WHERE car_id = %s;
        """
        cursor.execute(sql, [car_id])
        connection.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except Exception as e:
        connection.rollback()
        raise e

def insertModel(color, construction_year, transmission_type, car_id):
    try:
        sql = """
            INSERT INTO Model (color, construction_year, transmission_type, car_id)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(sql, [color, construction_year, transmission_type, car_id])
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e

def removeModel(model_id, car_id):
    try:
        sql = """
            DELETE FROM Model
            WHERE model_id = %s AND car_id = %s;
        """
        cursor.execute(sql, [model_id, car_id])
        connection.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except Exception as e:
        connection.rollback()
        raise e

def insertDriver(name, address_road_name, address_number, address_city):
    try:
        # try insert address
        try:
            sql = """
                INSERT INTO Address (road_name, number, city)
                VALUES (%s, %s, %s);
            """
            cursor.execute(sql, [address_road_name, address_number, address_city])
            connection.commit()
        except:
            connection.rollback()


        # insert driver
        sql = """
            INSERT INTO Driver (name, address_road_name, address_number, address_city)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(sql, [name, address_road_name, address_number, address_city])
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e

def removeDriver(name):
    try:
        sql = """
            DELETE FROM Driver
            WHERE name = %s;
        """
        cursor.execute(sql, [name])
        connection.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except Exception as e:
        connection.rollback()
        raise e

def getTopKClients(k):
    sql = """
        SELECT Client.email, Client.name, COUNT(Rent.rent_id) AS num_rents
        FROM Client
        JOIN Rent ON Client.email = Rent.client_email
        GROUP BY Client.email
        ORDER BY num_rents DESC
        LIMIT %s;
    """

    cursor.execute(sql, [k])
    data = cursor.fetchall()
    return [{
        "email": item[0],
        "name": item[1],
        "num_rents": item[2]
    } for item in data]

def getAllModelsWithNumRent():
    sql = """
        (
            SELECT model_id, color, construction_year, transmission_type, car_id, COUNT(rent_id) AS num_rents
            FROM Model
            NATURAL JOIN Rent
            GROUP BY model_id, car_id
            ORDER BY num_rents DESC
        )
        UNION
        (
            SELECT Model.model_id, color, construction_year, transmission_type, Model.car_id, 0 AS num_rents
            FROM Model
            LEFT JOIN Rent ON Model.model_id = Rent.model_id AND Model.car_id = Rent.car_id
            WHERE rent_id IS NULL
        );
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    return [{
        "model_id": item[0],
        "color": item[1],
        "construction_year": item[2],
        "transmission_type": item[3],
        "car_id": item[4],
        "num_rents": item[5]
    } for item in data]

def getAllDriversWithRentsAndAvgRating():
    sql = """
        WITH driverNumRent AS (
            (
                SELECT name, COUNT(rent_id) AS num_rents
                FROM Driver
                JOIN Rent ON Driver.name = Rent.driver_name
                GROUP BY name
            )
            UNION
            (
                SELECT name, 0 AS num_rents
                FROM Driver
                LEFT JOIN Rent ON Driver.name = Rent.driver_name
                WHERE rent_id IS NULL
            )
        ),
        driverAvgRating AS (
            (
                SELECT name, AVG(rating) AS avg_rating
                FROM Driver
                JOIN Review ON Driver.name = Review.driver_name
                GROUP BY name
            )
            UNION
            (
                SELECT name, -1 AS avg_rating
                FROM Driver
                LEFT JOIN Review ON Driver.name = Review.driver_name
                WHERE review_id IS NULL
            )
        )
        SELECT name, num_rents, avg_rating
        FROM driverNumRent
        NATURAL JOIN driverAvgRating;
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    return [{
        "name": item[0],
        "num_rents": item[1],
        "avg_rating": item[2]
    } for item in data]

def getTwoCityClients(clientCity, driverCity):
    sql = """
        SELECT Client.email, Client.name
        FROM Client
        JOIN Rent ON Client.email = Rent.client_email
        JOIN Driver ON Driver.name = Rent.driver_name
        JOIN ClientResidesAddress ON Client.email = ClientResidesAddress.client_email
        WHERE ClientResidesAddress.address_city = %s AND Driver.address_city = %s;
    """

    cursor.execute(sql, [clientCity, driverCity])
    data = cursor.fetchall()
    return [{
        "email": item[0],
        "name": item[1],
    } for item in data]

def registerClient(name, email):
    cursor.execute("INSERT INTO Client (name, email) VALUES (%s, %s);", (name, email))
    connection.commit()

def insertClientAddress(email, address):
    # Parse address into parts if needed
    road, number, city = address.split(",")  # assume "road,number,city"
    cursor.execute("INSERT INTO Address (road_name, number, city) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", (road, number, city))
    cursor.execute("INSERT INTO ClientResidesAddress (client_email, address_road_name, address_number, address_city) VALUES (%s, %s, %s, %s);", (email, road, number, city))
    connection.commit()

def insertCreditCard(card_number, email, cc_address):
    road, number, city = cc_address.split(",")
    cursor.execute("INSERT INTO Address (road_name, number, city) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", (road, number, city))
    cursor.execute("INSERT INTO CreditCard (credit_card_number, client_email, address_road_name, address_number, address_city) VALUES (%s, %s, %s, %s, %s);", (card_number, email, road, number, city))
    connection.commit()

def getClient(email):
    cursor.execute("SELECT name FROM Client WHERE email = %s;", (email,))
    result = cursor.fetchone()
    return {"name": result[0]} if result else None

def getAvailableModels(date):
    cursor.execute("""
        SELECT M.model_id, M.car_id, M.color, M.construction_year, M.transmission_type
        FROM Model M
        WHERE NOT EXISTS (
            SELECT 1
            FROM Rent R
            WHERE R.model_id = M.model_id AND R.car_id = M.car_id AND R.date = %s
        );
    """, (date,))
    rows = cursor.fetchall()
    return [{
        "model_id": r[0],
        "car_id": r[1],
        "color": r[2],
        "construction_year": r[3],
        "transmission_type": r[4]
    } for r in rows]


def bookRent(client_email, model_id, car_id, date):
    try:
        # Step 1: Check if this model is already booked on this date
        cursor.execute("""
            SELECT 1 FROM Rent
            WHERE model_id = %s AND car_id = %s AND date = %s;
        """, (model_id, car_id, date))
        if cursor.fetchone():
            return False  # Already booked

        # Step 2: Find a driver who can drive this model and is free on that date
        cursor.execute("""
            SELECT driver_name
            FROM DriverDrivesModel
            WHERE model_id = %s AND car_id = %s
            AND driver_name NOT IN (
                SELECT driver_name FROM Rent WHERE date = %s
            )
            LIMIT 1;
        """, (model_id, car_id, date))
        driver = cursor.fetchone()
        if not driver:
            return False  # No available driver

        # Step 3: Insert rent
        cursor.execute("""
            INSERT INTO Rent (client_email, model_id, car_id, driver_name, date)
            VALUES (%s, %s, %s, %s, %s);
        """, (client_email, model_id, car_id, driver[0], date))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print("Booking failed:", e)
        return False


def bookWithBestDriver(client_email, model_id, car_id, date):
    cursor.execute("""
        SELECT DDM.driver_name FROM DriverDrivesModel DDM
        LEFT JOIN (
            SELECT driver_name, AVG(rating) AS avg_rating FROM Review GROUP BY driver_name
        ) Rev ON DDM.driver_name = Rev.driver_name
        WHERE DDM.model_id = %s AND DDM.car_id = %s AND DDM.driver_name NOT IN (
            SELECT driver_name FROM Rent WHERE date = %s
        )
        ORDER BY COALESCE(avg_rating, -1) DESC
        LIMIT 1;
    """, (model_id, car_id, date))
    driver = cursor.fetchone()
    if not driver:
        return False
    cursor.execute("INSERT INTO Rent (client_email, model_id, car_id, driver_name, date) VALUES (%s, %s, %s, %s, %s);", (client_email, model_id, car_id, driver[0], date))
    connection.commit()
    return True

def getClientRents(email):
    cursor.execute("""
        SELECT R.date, CONCAT(M.color, ' ', M.transmission_type), R.driver_name
        FROM Rent R
        JOIN Model M ON R.model_id = M.model_id AND R.car_id = M.car_id
        WHERE R.client_email = %s
        ORDER BY R.date DESC;
    """, (email,))
    rows = cursor.fetchall()
    return [{"date": r[0], "model": r[1], "driver": r[2]} for r in rows]

def hasClientRentedFromDriver(email, driver_name):
    cursor.execute("SELECT 1 FROM Rent WHERE client_email = %s AND driver_name = %s LIMIT 1;", (email, driver_name))
    return cursor.fetchone() is not None

def insertReview(driver_name, client_email, rating, message):
    cursor.execute("INSERT INTO Review (driver_name, client_email, rating, message) VALUES (%s, %s, %s, %s);", (driver_name, client_email, rating, message))
    connection.commit()


def checkCarDeclaredByAnyDriver(car_id):
    sql = """
        SELECT driver_name
        FROM DriverDrivesModel
        WHERE car_id = %s;
    """

    cursor.execute(sql, [car_id])
    data = cursor.fetchone()
    if data:
        return True
    return False

def checkModelDeclaredByAnyDriver(model_id, car_id):
    sql = """
        SELECT driver_name
        FROM DriverDrivesModel
        WHERE model_id = %s AND car_id = %s;
    """

    cursor.execute(sql, [model_id, car_id])
    data = cursor.fetchone()
    if data:
        return True
    return False