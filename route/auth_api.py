from typing import Optional
from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from datetime import timedelta
from data.model import Account
from data.schema import account_schema

auth_api = Blueprint("auth_api", __name__)


@auth_api.post("/login")
def login():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    account: Optional[Account] = Account.objects(name__exact=username).first()
    if not account or not account.check_password(password):
        return jsonify("User does not exits or incorrect password"), 401

    exp_timestamp: timedelta = app.config["JWT_ACCESS_TOKEN_EXPIRES"]

    res = account_schema.dump(account)
    res["token_lifespan_seconds"] = (
        exp_timestamp.seconds if isinstance(exp_timestamp, timedelta) else exp_timestamp
    )
    res["access_token"] = create_access_token(identity=account)
    res["refresh_token"] = create_refresh_token(identity=account)

    return res


@auth_api.post("/refresh")
@jwt_required(refresh=True)
def refresh_access_token():
    current_user = get_jwt_identity()

    exp_timestamp: timedelta = app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    return {
        "access_token": create_access_token(identity=current_user),
        "refresh_token": create_refresh_token(identity=current_user),
        "token_lifespan_seconds": exp_timestamp.seconds
        if isinstance(exp_timestamp, timedelta)
        else exp_timestamp,
    }
