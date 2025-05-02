from flask import Blueprint, render_template, request, session, redirect, jsonify
from database.db import cursor, connection
from database import db_utils  # Assumes you have utility functions here

client = Blueprint("client", __name__, url_prefix="/client")

@client.route("/")
def index():
    if "client" in session:
        return redirect("/client/home")
    return render_template("/client/index.html")

@client.route("/home")
def home():
    if "client" not in session:
        return redirect("/client")
    client_data = db_utils.getClient(session["client"])
    return render_template("/client/home.html", name=client_data["name"])

@client.route("/register", methods=["POST"])
def register():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        address = request.form.get("address")
        cc_address = request.form.get("cc_address")
        cc_number = request.form.get("cc_number")

        db_utils.registerClient(name, email)
        db_utils.insertClientAddress(email, address)
        db_utils.insertCreditCard(cc_number, email, cc_address)

        session["client"] = email
        return "", 200
    except Exception as e:
        connection.rollback()
        print("Registration error:", e)
        return "", 500
    
@client.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            data = db_utils.getClient(email)
            if not data:
                return "Account does not exist", 400
            
            # create session
            print("Logged in:", data)
            session["client"] = email
            
            return "", 200
        except Exception as e:
            print("Client login error:", e)
            return "", 500
    else:
        return "Bad request", 400


@client.route("/logout")
def logout():
    session.pop("client")
    return redirect("/client")

@client.route("/availableModels", methods=["POST"])
def availableModels():
    try:
        date = request.form.get("date")
        models = db_utils.getAvailableModels(date)
        return jsonify(models)
    except Exception as e:
        print("Error fetching available models:", e)
        return "", 500

@client.route("/bookRent", methods=["POST"])
def bookRent():
    try:
        model_id = int(request.form.get("model_id"))
        car_id = int(request.form.get("car_id"))
        date = request.form.get("date")
        email = session.get("client")

        print(f"Attempting booking: {email=}, {model_id=}, {car_id=}, {date=}")

        success = db_utils.bookRent(email, model_id, car_id, date)
        if not success:
            return "No available model or driver", 400
        return "", 200
    except Exception as e:
        print("Booking error:", e)
        return "", 500

@client.route("/bookBestDriver", methods=["POST"])
def bookBestDriver():
    try:
        model_id = int(request.form.get("model_id"))
        car_id = int(request.form.get("car_id"))
        date = request.form.get("date")
        email = session.get("client")

        success = db_utils.bookWithBestDriver(email, model_id, car_id, date)
        if not success:
            return "No available model or best driver", 400
        return "", 200
    except Exception as e:
        print("Best driver booking error:", e)
        return "", 500

@client.route("/rents")
def getRents():
    try:
        email = session.get("client")
        rents = db_utils.getClientRents(email)
        return jsonify(rents)
    except Exception as e:
        print("Rent history error:", e)
        return "", 500

@client.route("/review", methods=["POST"])
def submitReview():
    try:
        email = session.get("client")
        driver_name = request.form.get("driver_name")
        rating = int(request.form.get("rating"))
        message = request.form.get("message")

        if db_utils.hasClientRentedFromDriver(email, driver_name):
            db_utils.insertReview(driver_name, email, rating, message)
            return "", 200
        else:
            return "You cannot review a driver you haven't rented from.", 400
    except Exception as e:
        print("Review error:", e)
        return "", 500
