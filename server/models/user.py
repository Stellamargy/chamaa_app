from sqlalchemy import Integer, String,Boolean
from sqlalchemy.orm import Mapped, mapped_column
from server.models.basemodel import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    __tablename__="users"
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email_address: Mapped[str] = mapped_column(String(100), nullable=False,unique=True)
    _password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_verified:Mapped[str]=mapped_column(Boolean,nullable=False,default=False)


    @property
    def password(self):
        raise AttributeError("Password is write-only")  # Cannot read
    # Hash password from plain text when creating a user instance - security  
    @password.setter
    def password(self, plain_text):
        self._password_hash = generate_password_hash(plain_text)
    