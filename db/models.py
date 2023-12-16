from sqlalchemy import (
    Integer,
    BigInteger,
    Text,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base


class Manhva(Base):
    __tablename__ = "manhva"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    manhva_name = mapped_column(Text, nullable=False)
    user_details: Mapped[list["ManhvaUserAssociation"]] = relationship(
        back_populates="manhva", lazy='selectin'
    )


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(BigInteger, nullable=False, index=True)
    manhva_details: Mapped[list["ManhvaUserAssociation"]] = relationship(
        back_populates="user", lazy='selectin'
    )


class ManhvaUserAssociation(Base):
    __tablename__ = "manhva_user_association"
    __table_args__ = (
        UniqueConstraint("manhva_id", "user_id", name="idx_unique_manhva_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manhva_id: Mapped[int] = mapped_column(ForeignKey("manhva.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="manhva_details", lazy='selectin')
    manhva: Mapped["Manhva"] = relationship(back_populates="user_details", lazy='selectin')
