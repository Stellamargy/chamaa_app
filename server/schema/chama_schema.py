from marshmallow import Schema, fields, validate, validates, ValidationError
class ChamaSchema(Schema):
    name =fields.String(
        required=True,
        allow_none=False,
        validate=validate.Length(max=100)
        )
    description=fields.String(
        allow_none=True,
        load_default=None, 
        validate=validate.Length(max=200)
        )
    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Chama name cannot be blank.")
    



