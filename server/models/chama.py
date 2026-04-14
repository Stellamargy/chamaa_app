import enum
from sqlalchemy import Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from server.models.basemodel import BaseModel


class ChamaStatus(str, enum.Enum):
    """
    Lifecycle states for a chama.

    ACTIVE     → default state on creation. Group is fully operational.
    INACTIVE   → soft delete. The group is hidden from normal queries
                 but all data (members, contributions, wallet) is preserved.
    SUSPENDED  → reserved for subscription enforcement. A chama moves here
                 when a subscription payment fails or lapses. Read-only access
                 only — no contributions or invites until payment is resolved.
    """
    ACTIVE    = "active"
    INACTIVE  = "inactive"
    SUSPENDED = "suspended"


class Chama(BaseModel):
    """
    Represents a chama (savings group).

    A chama is created by one user (the founder) who self-assigns
    their role during creation. The group comes into existence immediately
    — there is no draft or pending state.

    Constraints enforced at the application layer:
      - At least one ACTIVE member must hold INVITE_MEMBERS permission
        before the founder is allowed to leave.
      - Contributions cannot run without a contribution rule set.
      - Wallet transactions cannot run without a linked ChamaWallet.
      - A SUSPENDED chama blocks all write operations until
        the subscription is resolved.
    """
    __tablename__ = "chamas"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Tracks the chama's lifecycle. Defaults to ACTIVE on creation.
    # Use this for soft deletes (INACTIVE) and subscription enforcement (SUSPENDED).
    # Never hard-delete a chama — financial history must be preserved.
    status: Mapped[ChamaStatus] = mapped_column(
        Enum(ChamaStatus), nullable=False, default=ChamaStatus.ACTIVE
    )

    # The user who created this chama.
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    # --- Relationships ---

    members: Mapped[list["ChamaMember"]] = relationship(
        "ChamaMember", back_populates="chama", cascade="all, delete-orphan"
    )
    creator: Mapped["User"] = relationship(
        "User", back_populates="chamas_created"
    )
    wallet: Mapped["ChamaWallet"] = relationship(
        "ChamaWallet", back_populates="chama", cascade="all, delete-orphan", uselist=False
    )