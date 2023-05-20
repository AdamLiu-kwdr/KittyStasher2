from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import MongoEngine
from mongoengine import (
    Document,
    DynamicDocument,
    StringField,
    DateTimeField,
    FileField,
)

db = MongoEngine()

class Account(Document):
    name = StringField(Required=True)
    pass_hash = StringField(Required=True)  # Password hash, NOT password itself.
    role = StringField()

    def check_password(self, password) -> bool:
        return check_password_hash(self.pass_hash, password)

    def modify_password_hash(self, password):
        self.pass_hash = generate_password_hash(password)


class Record(DynamicDocument):
    picture_url = StringField()
    video_url = StringField()
    extra_notes = StringField()
    uploader_name = StringField()
    upload_datetime = DateTimeField()
    meta = {'strict': False} # Allows extra optional fields for extension


# TODO: feed password from env!
def seed_data(db):
    from datetime import datetime
    if Account.objects().count() == 0:
        new_admin = Account(name = "admin",role = "admin")
        new_admin.modify_password_hash("default_password")
        new_admin.save()
