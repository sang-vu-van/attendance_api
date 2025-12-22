from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from chalicelib.models.base import Base

if TYPE_CHECKING:
    from chalicelib.models.project import Project


class User(Base):
    """Class representing a person"""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()  # pylint: disable=not-callable
    )
    projects: Mapped[list["Project"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    def __init__(self, username: str):
        self.username = username
