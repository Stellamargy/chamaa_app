from decimal import Decimal
from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from server.models.basemodel import BaseModel


class ChamaWallet(BaseModel):
    """
    Represents the shared money pool for a chama.
    Each chama has at most one wallet (enforced by unique=True on chama_id).

    The wallet is auto created during chama creation time .Contribution transactions and payouts
    are blocked at the application layer until a wallet is linked.

    Balance uses Numeric (fixed-point decimal) for precision.
    Float is intentionally avoided — floats accumulate rounding errors
    on repeated addition/subtraction, which is unacceptable for money.
    """
    __tablename__ = "chama_wallets"

    # One wallet per chama. unique=True enforces the one-to-one relationship.
    chama_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chamas.id"), nullable=False, unique=True
    )

    # Stored as fixed-point decimal. e.g. KES 1,450.75 → 1450.75
    # precision=12, scale=2 supports balances up to 9,999,999,999.99
   
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2), nullable=False, default=0
    )

    # --- Relationships ---

    # uselist=False is set on Chama.wallet to enforce one-to-one.
    chama: Mapped["Chama"] = relationship("Chama", back_populates="wallet",uselist=False)