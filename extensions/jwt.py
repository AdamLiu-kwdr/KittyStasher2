from flask_jwt_extended import JWTManager
from data.model import Account

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(account):
    return str(account.id)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    account = Account.objects(id=identity).first()
    return account
