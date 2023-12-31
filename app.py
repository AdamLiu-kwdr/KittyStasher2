from flask import Flask
from data.model import db, create_default_admin
from route.record_api import record_api
from route.auth_api import auth_api
from route.file_api import file_api
from route.account_api import account_api
from extensions.jwt import jwt


def create_app():
    app = Flask(__name__)

    # Default configurations for development
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 600
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": "kittystasher-dev",
            "host": "localhost",
            "port": 27017,
            "alias": "default",
        }
    ]

    app.config.from_prefixed_env()

    app.register_blueprint(record_api, url_prefix="/record")
    app.register_blueprint(file_api, url_prefix="/file")
    app.register_blueprint(account_api, url_prefix="/account")
    app.register_blueprint(auth_api)

    db.init_app(app)
    jwt.init_app(app)

    if app.debug == True:
        create_default_admin(db, "admin", "default_password")
    else:
        create_default_admin(
            db,
            app.config.get("KITTY_STASHER_ADMIN", "admin"),
            app.config.get("KITTY_STASHER_PASSWORD"),
        )

    return app
