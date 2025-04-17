from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///horus_abi_db.sqlite"
app.config["SECRET_KEY"] = "your_secret_key"
app.config["JWT_SECRET_KEY"] = "your_secret_key"

db = SQLAlchemy()
db.init_app(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

from routes import user_routes
app.register_blueprint(user_routes)

with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True)