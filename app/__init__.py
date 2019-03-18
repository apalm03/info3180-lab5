from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a secured key"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://apalm03:password111@localhost/project1"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://kpdrrutxqcnfgp:de2a060ff607e617f16029f3119665773973ab6acaac20fc5c4bc7d2668f99e3@ec2-23-23-241-119.compute-1.amazonaws.com:5432/d9geul9u3fhect"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
app.config['UPLOAD_FOLDER'] = './app/static/uploads'
db = SQLAlchemy(app)



app.config.from_object(__name__)
from app import views
