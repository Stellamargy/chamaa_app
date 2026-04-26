import enum
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from server.models.basemodel import BaseModel


class MemberRole(str, enum.Enum):
    """
    Predefined roles within a chama. The creator selects their own role
    at group creation time — nothing is auto-assigned.

    Roles control permissions at the application layer:
        CHAIRPERSON   → can invite members (INVITE_MEMBERS permission)
        SECRETARY     → no special permissions in V1 / permissions added later on
        TREASURER     → no special permissions in V1 / permissions added later on
        MEMBER        → no special permissions in V1 / permissions added later on

    The creator always retains the INVITE_MEMBERS override via is_creator=True,
    regardless of which role they chose.
    """
    CHAMA_ADMIN="chama_admin"
    CHAIRPERSON = "chairperson"
    SECRETARY = "secretary"
    TREASURER = "treasurer"
    MEMBER = "member"


class MemberStatus(str, enum.Enum):
    """
    Tracks the full lifecycle of a membership:

        PENDING  → invite sent, user has not yet accepted
        ACTIVE   → user accepted the invite, full group member
        LEFT     → user voluntarily exited the chama
        REMOVED  → user was removed by an authorised member
    """

    PENDING = "pending"
    ACTIVE = "active"
    LEFT = "left"
    REMOVED = "removed"


class ChamaMember(BaseModel):
    """
    Join table between User and Chama. Represents one person's
    membership in one chama — including their role, current status,
    whether they founded the group, and who invited them.

    A user can belong to many chamas, but can only have one
    membership record per chama (enforced by the unique constraint).
    """

    __tablename__ = "chama_members"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    chama_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chamas.id"), nullable=False
    )

    # Role the member holds in this chama.
    # Creator chooses their own role at creation time.
    role: Mapped[MemberRole] = mapped_column(
        Enum(MemberRole), nullable=False, default=MemberRole.MEMBER
    )

    # Membership lifecycle state (replaces the old is_active boolean).
    # Use this for all permission and access checks.
    status: Mapped[MemberStatus] = mapped_column(
        Enum(MemberStatus), nullable=False, default=MemberStatus.PENDING
    )


    # The member who sent this invite. NULL for the founding member
    # (they were never invited — they created the group).
    invited_by: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )

    # Timestamp of when the user moved from PENDING → ACTIVE.
    # NULL until they accept the invite.
    joined_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True,)

    # --- Relationships ---

    user: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id], back_populates="chama_memberships"
    )
    chama: Mapped["Chama"] = relationship("Chama", back_populates="members")

    # The member who sent this invitation (nullable, no back_populates needed).
    inviter: Mapped["User | None"] = relationship("User", foreign_keys=[invited_by])

    # --- Constraints ---

    __table_args__ = (
        # A user can only have one membership record per chama.
        # They can belong to many chamas, but not twice to the same one.
        UniqueConstraint("user_id", "chama_id", name="uq_user_chama_membership"),
    )
