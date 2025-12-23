from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime, func
from chalicelib.domain.models.base import Base

if TYPE_CHECKING:
    from chalicelib.models.project import Project


class Task(Base):
    """タスクの情報を表示"""

    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()  # pylint: disable=not-callable
    )
    project: Mapped["Project"] = relationship(back_populates="tasks")

    def __init__(self, title: str, project_id: int, detail: str | None = None):
        self.title = (title,)
        self.project_id = project_id
        self.detail = detail
