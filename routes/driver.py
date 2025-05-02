from flask import Blueprint, render_template, request, session, redirect, jsonify
from database.db import cursor, connection
from database import db_utils

driver = Blueprint("driver", __name__, url_prefix="/driver")

@driver.route("/")
def index():
    if session and "driver" in session:
        return redirect("/driver/home")
    return render_template("/driver/index.html")

@driver.route("/register", methods=["POST"])
def register():
    try:
        name = request.form.get("name")
        if not name:
            return "Name is required", 400

        # Check if driver already exists
        existing = db_utils.getDriver(name)
        if existing:
            return "Driver already exists", 400

        # Insert with dummy/default address since you no longer collect that
        db_utils.insertDriver(name, "Unknown", "0", "Unknown")
        return "", 200
    except Exception as e:
        print("Error registering driver:", e)
        return "", 500

@driver.route("/home")
def home():
    if session and "driver" in session:
        try:
            driver_name = session["driver"]
            driver_info = db_utils.getDriver(driver_name)
            models = db_utils.getAllModels()
            driven_models = db_utils.getModelsDrivenBy(driver_name)
            return render_template("/driver/home.html", driver=driver_info, models=models, driven=driven_models)
        except Exception as e:
            print(f"Error loading driver home: {e}")
            return "", 500
    return redirect("/driver")

@driver.route("/login", methods=["POST"])
def login():
    try:
        name = request.form.get("name")
        driver = db_utils.getDriver(name)
        if not driver:
            return "Driver not found", 400
        session["driver"] = name
        return "", 200
    except Exception as e:
        print("Login error:", e)
        return "", 500

@driver.route("/logout")
def logout():
    session.pop("driver", None)
    return "", 200

@driver.route("/updateAddress", methods=["POST"])
def updateAddress():
    try:
        name = session["driver"]
        road = request.form.get("address_road_name")
        number = request.form.get("address_number")
        city = request.form.get("address_city")
        db_utils.updateDriverAddress(name, road, number, city)
        return "", 200
    except Exception as e:
        print("Error updating address:", e)
        return "", 500

@driver.route("/declareModel", methods=["POST"])
def declareModel():
    try:
        name = session["driver"]
        model_id = int(request.form.get("model_id"))
        car_id = int(request.form.get("car_id"))
        db_utils.declareModelForDriver(name, model_id, car_id)
        return "", 200
    except Exception as e:
        print("Error declaring model:", e)
        return "", 500
