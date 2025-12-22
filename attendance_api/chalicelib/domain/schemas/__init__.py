# Gom schema để import ngắn gọn:
# from chalicelib.domain.schemas import UserCreateSchema, UserUpdateSchema, ...

from chalicelib.domain.schemas.user_schema import UserCreateSchema
from chalicelib.domain.schemas.user_update_schema import UserUpdateSchema

from chalicelib.domain.schemas.project_schema import ProjectCreateSchema
from chalicelib.domain.schemas.project_update_schema import ProjectUpdateSchema

from chalicelib.domain.schemas.task_schema import TaskCreateSchema
from chalicelib.domain.schemas.task_update_schema import TaskUpdateSchema

__all__ = [
    "UserCreateSchema",
    "UserUpdateSchema",
    "ProjectCreateSchema",
    "ProjectUpdateSchema",
    "TaskCreateSchema",
    "TaskUpdateSchema",
]
