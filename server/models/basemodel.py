from . import db
from sqlalchemy import Integer,DateTime ,func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
class BaseModel(db.Model):
    __abstract__ = True  # This tells SQLAlchemy not to create a table for this class(only exist to be inherited from )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime]=mapped_column(DateTime,nullable=False,server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=True,  # Allow NULL
        onupdate=func.now()  # Only set when actually updated
    )
   