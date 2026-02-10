from sqlalchemy import Integer, String,Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .basemodel import BaseModel

class User(BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email_address: Mapped[str] = mapped_column(String, nullable=False,unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_verified:Mapped[str]=mapped_column(Boolean,nullable=False,default=False)
    