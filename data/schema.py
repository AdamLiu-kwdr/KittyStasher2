from marshmallow_mongoengine import ModelSchema
from mongoengine import GridFSProxy
from marshmallow import INCLUDE, EXCLUDE, fields, post_dump, Schema
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

    # There's extra fields stored in mongodb. Add them back to output
    @post_dump(pass_original=True)
    def keep_unknowns(self, output, orig, **kwargs):
        for key in orig:
            if key not in output and not isinstance(orig[key], GridFSProxy):
                output[key] = orig[key]
        return output


account_schema = AccountSchema()
record_schema = RecordSchema()


# data_key is used for accepting input from URL parameters, and convert to mongodb query
class RecordQuerySchema(Schema):
    upload_datetime__gt = fields.DateTime(data_key="start_date")
    upload_datetime__lt = fields.DateTime(data_key="end_date")

    class Meta:
        unknown = EXCLUDE


record_query_schema = RecordQuerySchema()


# For pagination query from URL parameters
class PaginationSchema(Schema):
    page = fields.Integer()
    page_size = fields.Integer()

    class Meta:
        unknown = EXCLUDE


pagination_schema = PaginationSchema()
