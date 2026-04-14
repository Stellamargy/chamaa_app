from marshmallow import Schema, fields, validate, validates, ValidationError, pre_load
from server.models.chama_member import MemberRole


class CreateChamaSchema(Schema):
    """
    Validates the POST /chamas request body.
    The creator's role is required — nothing is auto-assigned.
    """

    @pre_load
    def normalize(self, data, **kwargs):
        # Normalize name
        if "name" in data and data["name"] is not None:
            data["name"] = data["name"].strip()

        # Normalize description
        if "description" in data:
            desc = data["description"]
            if desc is not None:
                desc = desc.strip()
                data["description"] = desc if desc else None  # "" → None

        return data

    name = fields.String(
        required=True,
        allow_none=False,
        validate=validate.Length(min=1, max=50)
    )
    
    description = fields.String(
        allow_none=True, 
        load_default=None,
        validate=validate.Length(max=200)
    )

    #creator role .
    role=fields.Enum(
        MemberRole,
        required=True,
        allow_none=False,
        by_value=True
    )


