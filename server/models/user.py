from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from server.models.basemodel import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email_address: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    # Targeted for Kenyan users
    phone_number: Mapped[str] = mapped_column(String(13), nullable=False, unique=True)
    _password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # getter for _password_hash (internal attribute)
    @property
    def password(self):
        return self._password_hash

    # setter for _password_hash - hashes plain text password for security
    @password.setter
    def password(self, plain_password):
        self._password_hash = generate_password_hash(plain_password)

    # Compare password hashes
    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)
