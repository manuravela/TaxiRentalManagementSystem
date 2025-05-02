from flask import Flask, render_template
from routes.manager import manager
from routes.driver import driver
from routes.client import client

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

@app.route("/")
def index():
    return render_template("index.html")

# register blueprints
app.register_blueprint(manager)
app.register_blueprint(driver)
app.register_blueprint(client)

if __name__ == "__main__":
    app.run(
        host="localhost",
        port=8000,
        debug=True,
    )