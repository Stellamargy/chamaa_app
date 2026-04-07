from .basemodel import BaseModel
from sqlalchemy import Integer, String, Boolean,Text
from sqlalchemy.orm import Mapped, mapped_column
class Chama(BaseModel):

    __tablename__="chamas"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    #relationships
    members = relationship("ChamaMember", back_populates="chama", cascade="all, delete-orphan")