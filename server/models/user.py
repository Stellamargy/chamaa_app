from sqlalchemy import Integer, String,Boolean
from sqlalchemy.orm import Mapped, mapped_column
from server.models.basemodel import BaseModel


class User(BaseModel):
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email_address: Mapped[str] = mapped_column(String(100), nullable=False,unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_verified:Mapped[str]=mapped_column(Boolean,nullable=False,default=False)
    