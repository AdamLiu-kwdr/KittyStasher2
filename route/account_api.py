from typing import Optional
from flask import Blueprint, Response, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_current_user
from marshmallow import ValidationError
from data.model import Account
from data.schema import account_schema

account_api = Blueprint("account_api",__name__)

@account_api.get('/<id>')
@jwt_required()
def get(id):
    account = Account.objects(id=id).first()
    if not account:
        return jsonify({"error":f"Account for id {id} not found"}), 404
    
    return account_schema.dump(account)

def check_login_role(role: str):
    account = get_current_user()
    if account.role != role:
        abort(403, jsonify({"error":f"Action not authorized, {role} account only."}))

@account_api.post('/')
@jwt_required()
def create():
    check_login_role("admin")

    req_json = request.get_json()
    account_name = req_json.get("name")
    password = req_json.get("password")
    role = req_json.get("role")

    if not account_name or not password:
        return jsonify({"error":"username or password required"}), 400
    
    new_account = Account(name= account_name, role= role)
    new_account.modify_password_hash(password=password)

    new_account.save()
    return account_schema.dump(new_account)
    
@account_api.put('/')
@jwt_required()
def update():
    check_login_role("admin")

    req_json = request.get_json()
    account_name = req_json.get("name")
    password = req_json.get("password")
    role = req_json.get("role")

    modify_account: Optional[Account] = Account.objects(name__exact=account_name).first()
    if modify_account == None:
        return jsonify({"error": f"Account with id {id} not found"}), 404

    if password:
        modify_account.modify_password_hash(password)

    if role:
        modify_account.role = role

    modify_account.save()
    return account_schema.dump(modify_account)

@account_api.delete("/<id>")
@jwt_required()
def delete(id: str):
    check_login_role("admin")

    del_account = Account.objects(id=id).first()
    if del_account == None:
        return jsonify({"error": f"Account with id {id} not found"}), 404

    del_account.delete()
    return Response(status=200)