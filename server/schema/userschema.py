import re
from marshmallow import fields, validate, ValidationError, pre_load, validates
from marshmallow_sqlalchemy import SQLAlchemySchema
from server.models.user import User


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
    #Fields to validate
    first_name = fields.String(required=True, allow_none=False)
    last_name = fields.String(required=True, allow_none=False)
    password = fields.String(
        required=True,
        allow_none=False,
        load_only=True,
        validate=validate.Length(min=6)
    )

    email_address = fields.Email(required=True, allow_none=False)
    phone_number = fields.String(required=True, allow_none=False)

    
    @pre_load
    def normalize_email_address(self, user_input, **kwargs):
        if "email_address" in user_input:
            user_input["email_address"] = user_input["email_address"].lower().strip()
        return user_input

    #Custom validations 
    @validates("first_name")
    def validate_first_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("First name cannot be blank.")

    @validates("last_name")
    def validate_last_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Last name cannot be blank.")

    @validates("password")
    def validate_password(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Password cannot be blank.")

        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$"
        if not re.match(pattern, value):
            raise ValidationError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter, one number, and one symbol."
            )

    @validates("phone_number")
    def validate_phone_number(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Phone number cannot be blank.")

        pattern = r"^\+254(7|1)\d{8}$"
        if not re.match(pattern, value):
            raise ValidationError(
                """Phone number must be a valid Kenyan phone number starting with +254 and 12 digits in total"""
            )            

