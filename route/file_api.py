import gridfs
from gridfs.errors import NoFile
from mongoengine import get_db
from flask_jwt_extended import jwt_required
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, request, jsonify, make_response, send_file

file_api = Blueprint("file_api", __name__)


@file_api.post("/")
def upload():
    db = get_db()
    gfs = gridfs.GridFS(db)
    res = []

    for key,file in request.files.items(multi=True):
        id = gfs.put(file, content_type=file.content_type, filename=file.filename)
        res.append({"file_name": file.filename, "url": f"/file/{id}"})

    return jsonify(res)


@file_api.get("/<id>")
def download(id: str):
    db = get_db()
    gfs = gridfs.GridFS(db)

    try:
        file = gfs.get(ObjectId(id))
    except InvalidId:
        return jsonify({"error": "Invalid mongodb id"}), 400
    except NoFile:
        return jsonify({"error": f"file not found for id {id}"}), 404

    response = send_file(file, download_name=file.filename, mimetype=file.content_type)
    response.headers["Content-Type"] = file.content_type

    return response
