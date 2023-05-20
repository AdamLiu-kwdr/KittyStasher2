from marshmallow_mongoengine import ModelSchema
from mongoengine import GridFSProxy
from marshmallow import INCLUDE, EXCLUDE, fields, post_dump
from data.model import Account, Record

class AccountSchema(ModelSchema):
    class Meta:
        model = Account
        exclude = ("pass_hash",)
        unknown = EXCLUDE

class RecordSchema(ModelSchema):
    id = fields.Str(dump_only=True)
    class Meta:
        model = Record
        unknown = INCLUDE

    # Add extra fields back into output
    # @post_dump(pass_original=True)
    # def keep_unknowns(self, output, orig, **kwargs):
    #     for key in orig:
    #         if key not in output and not isinstance(orig[key],GridFSProxy):
    #             output[key] = orig[key]
    #     return output

account_schema = AccountSchema()
record_schema = RecordSchema()