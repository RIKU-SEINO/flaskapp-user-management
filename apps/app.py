from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from apps.config import config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "auth.signup"
login_manager.login_message = ""

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    db.init_app(app)
    Migrate(app,db)
    login_manager.init_app(app)

    from apps.crud import views as crud_views
    from apps.auth import views as auth_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    
    return app