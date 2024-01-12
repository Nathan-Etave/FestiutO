from sqlalchemy import create_engine, text
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['SECRET_KEY'] = "f1230e8f-9a89-4e23-9a3f-235539816b8f"
csrf = CSRFProtect(app)
csrf.init_app(app)

import festiuto.views
import festiuto.models
import festiuto.requetes
