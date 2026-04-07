from .basemodel import BaseModel
from sqlalchemy import Integer, String, Boolean,Text,DateTime,func,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
class ChamaMember(BaseModel):
    
    __tablename__="chama_members"
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id") ,nullable=False)
    chama_id:Mapped[int]=mapped_column(Integer,ForeignKey("chamas.id"),nullable=False)
    role:Mapped[str]=mapped_column(String,nullable=False,default="MEMBER") # ADMIN/MEMBER
    is_active:Mapped[bool]=mapped_column(Boolean,nullable=False,default=True)
    joined_at:Mapped[datetime]=mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    #Relationships 
    user = relationship("User", back_populates="chama_memberships")
    chama = relationship("Chama", back_populates="members")
    #Addition rules applied to the constraint table 
    __table_args__ = (
    UniqueConstraint("user_id", "chama_id", name="uq_user_chama_membership"),
    )
   