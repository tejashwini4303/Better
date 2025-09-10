from flask import Flask
from models import db
from routes import routes

app = Flask(__name__)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///better.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(routes)  # Register routes

@app.route("/")
def home():
    return "Flask backend with DB & CRUD APIs is running!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
