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


    
    #test


schema = CreateChamaSchema()

def test_input(data, label):
    print(f"\n--- {label} ---")
    try:
        result = schema.load(data)
        print("VALID ✅")
        print(result)
        print("Role type:", type(result["role"]))
        print("Role value:", result["role"].value)
    except ValidationError as err:
        print("INVALID ❌")
        print(err.messages)


# # 1. Valid input
# test_input(
#     {
#         "name": "  My Chama  ",
#         "description": "  Saving group  ",
#         "role": "chairperson"
#     },
#     "Valid input"
# )

# 2. Empty description (should become None)
test_input(
    {
        "name": "Group A",
        "description": "   ",
        "role": "member"
    },
    "Empty description → None"
)

# 3. Missing description (tests load_default)
test_input(
    {
        "name": "Group B",
        "role": "treasurer"
    },
    "Missing description"
)

# 4. Invalid role
test_input(
    {
        "name": "Group C",
        "role": "boss"
    },
    "Invalid role"
)

# 5. Blank name (after strip → should fail)
test_input(
    {
        "name": "   ",
        "role": "secretary"
    },
    "Blank name"
)

# 6. Name too long
test_input(
    {
        "name": "A" * 60,
        "role": "member"
    },
    "Name too long"
)





