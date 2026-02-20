# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,validate
from server.models.user import User
from marshmallow import validates, ValidationError,pre_load
from marshmallow_sqlalchemy import SQLAlchemySchema,auto_field

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        # exclude = ("password_hash","id","created_at","updated_at")

    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    email_address = fields.Email(required=True)

    #Run this fn to normalize email address before schema level validation 
    @pre_load
    def normalize_email_address(self,user_input,**kwargs):
        if "email_address" in user_input:
            user_input["email_address"]=user_input["email_address"].lower().strip()
        return user_input
   
    @validates("first_name")
    def validate_first_name(self, value,**kwargs):
        if not value.strip():
            raise ValidationError("First name cannot be blank.")

    @validates("last_name")
    def validate_last_name(self, value,**kwargs):
        if not value.strip():
            raise ValidationError("Last name cannot be blank.")

    @validates("password")
    def validate_password(self, value,**kwargs):
        if not value.strip():
            raise ValidationError("Password  cannot be blank.")        
