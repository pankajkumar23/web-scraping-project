from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from database.db import db
import os
from routes.main_router import main_router
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)
load_dotenv()
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.register_blueprint(main_router)
db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app,db)
app.json.sort_keys = False
@app.route("/index")
def index():
    return {"message":"server is running"}

if __name__ =="__main__":
    app.run(debug=True)