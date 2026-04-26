#USER MODEL
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from server.models.basemodel import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    """
    Represents an application user.
    A user can create chamas (as the founding member) and belong
    to many chamas through the ChamaMember join table.
    Targeted at Kenyan users — phone numbers follow the +254 format.
    """
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email_address: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    # Kenyan phone numbers: +254XXXXXXXXX (13 chars including country code)
    phone_number: Mapped[str] = mapped_column(String(13), nullable=False, unique=True)

    _password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # True once the user confirms their email address.
    # Unverified users should have restricted access.
   
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Soft-delete flag. Deactivated users cannot log in
    # but their data (contributions, memberships) is preserved.
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # --- Relationships ---

    # All chama memberships this user holds (across all groups).
    # Deleting a user cascades to remove their membership records.
    chama_memberships: Mapped[list["ChamaMember"]] = relationship(
        "ChamaMember", back_populates="user", cascade="all, delete-orphan",
        foreign_keys="ChamaMember.user_id"
    )

    # All chamas this user has founded.
    # back_populates must match the attribute name on Chama ("creator").
    chamas_created: Mapped[list["Chama"]] = relationship(
        "Chama", back_populates="creator", cascade="all, delete-orphan"
    )

    # --- Password helpers ---

    @property
    def password(self) -> str:
        """Returns the stored password hash. Never the plain-text password."""
        return self._password_hash

    @password.setter
    def password(self, plain_password: str) -> None:
        """Accepts a plain-text password and stores it as a bcrypt hash."""
        self._password_hash = generate_password_hash(plain_password)

    def check_password(self, plain_password: str) -> bool:
        """Returns True if plain_password matches the stored hash."""
        return check_password_hash(self._password_hash, plain_password)
