from flask import Blueprint, render_template, request, session, redirect, jsonify
from database.db import cursor
from database.db import connection
from database import db_utils

manager = Blueprint("manager", __name__, url_prefix="/manager")

@manager.route("/")
def index():
    if session and "manager" in session:
        return redirect("/manager/home")
    return render_template("/manager/index.html")

@manager.route("/home")
def home():
    if session and "manager" in session:
        try:
            manager = db_utils.getManager(session["manager"])
            cars = db_utils.getAllCars()
            models = db_utils.getAllModelsWithNumRent()
            drivers = db_utils.getAllDriversWithRentsAndAvgRating()
            return render_template("/manager/home.html", name=manager["name"], cars=cars, models=models, drivers=drivers)
        except Exception as e:
            print(f"Something is wrong with getting manager: {e}")
            return "", 500
    
    return redirect("/manager")

@manager.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            ssn = request.form.get("ssn")
            email = request.form.get("email")
            
            sql = """
                INSERT INTO Manager (name, ssn, email)
                VALUES (%s, %s, %s);
            """
            cursor.execute(sql, [name, ssn, email])

            # commit connection
            connection.commit()

            print(f"Registered: name: {name}, ssn: {ssn}, email: {email}")

            # create session
            session["manager"] = ssn

            return "", 200
        except Exception as e:
            # Rolling back the transaction in case of error
            connection.rollback()
            print(f"Transaction rolled back due to error: {e}")
            return "", 500
    else:
        return "Bad request", 400
    
@manager.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        try:
            ssn = request.form.get("ssn")
            data = db_utils.getManager(ssn)
            if not data:
                return "Account not exists", 400
            
            # create session
            print("Logined:", data)
            session["manager"] = data["ssn"]
            
            return "", 200
        except Exception as e:
            print(f"Something is wrong with getting manager: {e}")
            return "", 500
        
    else:
        return "Bad request", 400

@manager.route("/logout")
def logout():
    session.pop("manager")
    
    return "", 200

@manager.route("/insertCar", methods=["POST"])
def insertCar():
    try:
        brand = request.form.get("brand")
        db_utils.insertCar(brand)
        return "", 200
    except Exception as e:
        print("Something is wrong with inserting car", e)
        return "", 500

@manager.route("/removeCar", methods=["POST"])
def removeCar():
    try:
        car_id = int(request.form.get("car_id"))
        if db_utils.removeCar(car_id):
            return "", 200
        else:
            print("Remove no car")
            return "Remove no car", 400
    except Exception as e:
        print("Something is wrong with removing car", e)
        return "", 500
    
@manager.route("/insertModel", methods=["POST"])
def insertModel():
    try:
        color = request.form.get("color")
        construction_year = int(request.form.get("construction_year"))
        transmission_type = request.form.get("transmission_type")
        car_id = int(request.form.get("car_id"))
        db_utils.insertModel(color, construction_year, transmission_type, car_id)
        return "", 200
    except Exception as e:
        print("Something is wrong with inserting model", e)
        return "", 500

@manager.route("/removeModel", methods=["POST"])
def removeModel():
    try:
        model_id = int(request.form.get("model_id"))
        car_id = int(request.form.get("car_id"))
        if db_utils.removeModel(model_id, car_id):
            return "", 200
        else:
            print("Remove no model")
            return "Remove no model", 400
    except Exception as e:
        print("Something is wrong with removing model", e)
        return "", 500

@manager.route("/insertDriver", methods=["POST"])
def insertDriver():
    try:
        name = request.form.get("name")
        address_road_name = request.form.get("address_road_name")
        address_number = request.form.get("address_number")
        address_city = request.form.get("address_city")
        db_utils.insertDriver(name, address_road_name, address_number, address_city)
        return "", 200
    except Exception as e:
        print("Something is wrong with inserting driver", e)
        return "", 500

@manager.route("/removeDriver", methods=["POST"])
def removeDriver():
    try:
        name = request.form.get("name")
        if db_utils.removeDriver(name):
            return "", 200
        else:
            print("Remove no driver")
            return "Remove no driver", 400
    except Exception as e:
        print("Something is wrong with removing driver", e)
        return "", 500

@manager.route("/topClients", methods=["POST"])
def getTopKClients():
    try:
        k = int(request.form.get("k"))
        clients = db_utils.getTopKClients(k)
        return jsonify({
            "clients": clients
        })
    except Exception as e:
        print("Something is wrong with getting top k clients", e)
        return "", 500
    
@manager.route("/twoCityClients", methods=["POST"])
def getTwoCityClients():
    try:
        clientCity = request.form.get("clientCity")
        driverCity = request.form.get("driverCity")
        clients = db_utils.getTwoCityClients(clientCity, driverCity)
        return jsonify({
            "clients": clients
        })
    except Exception as e:
        print("Something is wrong with getting two city clients", e)
        return "", 500