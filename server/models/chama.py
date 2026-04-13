from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from server.models.basemodel import BaseModel


class Chama(BaseModel):
    """
    Represents a chama (savings group).

    A chama is created by one user (the founder) who self-assigns
    their role during creation. The group comes into existence immediately
    — there is no draft state. Members are added progressively via invites.

    Constraints enforced at the application layer (not DB):
      - At least one ACTIVE member must hold INVITE_MEMBERS permission
        before the founder is allowed to leave.
      - Contributions cannot run without a contribution rule set.
      - Wallet transactions cannot run without a linked ChamaWallet.
    """
    __tablename__ = "chamas"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # The user who created this chama. Used for the creator override
    # in permission checks (see ChamaMember.is_creator for the cleaner approach).
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    # --- Relationships ---

    # All current and past members of this chama.
    members: Mapped[list["ChamaMember"]] = relationship(
        "ChamaMember", back_populates="chama", cascade="all, delete-orphan"
    )

    # The user who founded this chama.
    # back_populates must match the attribute name on User ("chamas_created").
    creator: Mapped["User"] = relationship(
        "User", back_populates="chamas_created"
    )

    # A chama has exactly one wallet (one-to-one, enforced by unique=True on FK).
    # Wallet is created separately during chama creation .
    wallet: Mapped["ChamaWallet"] = relationship(
        "ChamaWallet", back_populates="chama", cascade="all, delete-orphan", uselist=False
    )