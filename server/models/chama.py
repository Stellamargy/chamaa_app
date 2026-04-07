from .basemodel import BaseModel
from sqlalchemy import Integer, String, Boolean,Text,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
class Chama(BaseModel):

    __tablename__="chamas"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_by:Mapped[int]=mapped_column(Integer,ForeignKey("users.id"),nullable=False)
    #relationships
    members = relationship("ChamaMember", back_populates="chama", cascade="all, delete-orphan")
    creator=relationship("User",back_populates="chamas")