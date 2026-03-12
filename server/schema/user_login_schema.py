from marshmallow import Schema, fields, validate, validates, ValidationError, pre_load


class UserLoginSchema(Schema):

    # Login credentials(or fields to validate) are email_address and password
    email_address = fields.Email(required=True, allow_none=False)
    password = fields.String(
        required=True, allow_none=False, validate=validate.Length(min=6)
    )

    # Normalize email - lowercase, no trailing white spaces (important for handling uniqueness)
    @pre_load
    def normalize_email_address(self, user_input, **kwargs):
        if "email_address" in user_input:
            user_input["email_address"] = user_input["email_address"].lower().strip()
        return user_input

    @validates("password")
    def validate_password(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Password cannot be blank.")
