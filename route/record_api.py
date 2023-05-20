from typing import Optional
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user
from marshmallow import ValidationError
from datetime import datetime

from data.model import Record
from data.schema import RecordSchema, record_schema

record_api = Blueprint("record_api", __name__)


@record_api.get("/")
def get_all():
    records = Record.objects()
    res = record_schema.dump(records, many=True)
    return res


@record_api.get("/<id>")
def get_by_id(id: str):
    record: Optional[Record] = Record.objects(id=id).first()
    if not record:
        return jsonify(f"Record not found for record {id}"), 404
    return record_schema.dump(record)


@record_api.post("/")
@jwt_required()
def create():
    try:
        new_record: Record = record_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Due to record has unknown=INCLUDE, have to remove id here
    delattr(new_record, "id")

    uploader = get_current_user()
    new_record.uploader_name = uploader.name

    new_record.upload_datetime = datetime.now()
    new_record.save()
    return record_schema.dump(new_record)


# Attribute not inside request json will get deleted.
@record_api.put("/")
@jwt_required()
def update():
    try:
        record_schema = RecordSchema()
        modify_record: Record = record_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    modify_record.upload_datetime = datetime.now()
    modify_record.save()
    return record_schema.dump(modify_record)


@record_api.delete("/<id>")
@jwt_required()
def delete(id: str):
    del_record = Record.objects(id=id)[0]
    if del_record == None:
        return jsonify({"error": f"Record with id {id} not found"}), 404

    del_record.delete()
    return Response(status=200)
