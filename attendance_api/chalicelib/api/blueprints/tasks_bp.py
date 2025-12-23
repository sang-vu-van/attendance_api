from chalice import Blueprint
from chalicelib.core.db import SessionLocal
from chalicelib.core import json_error, json_ok
from chalicelib.core.validators import validate_json, parse_int_param
from chalicelib.domain.models import Project, Task
from chalicelib.domain.schemas import TaskCreateSchema, TaskUpdateSchema

bp_tasks = Blueprint(__name__)
schema_create = TaskCreateSchema()
schema_update = TaskUpdateSchema()


@bp_tasks.route("/tasks", methods=["POST"])
def create_task():
    """
    create_task API
    """
    data = validate_json(schema_create, bp_tasks.current_request)
    if not isinstance(data, dict):
        return data
    db = SessionLocal()
    try:
        project_data = db.get(Project, data["project_id"])
        if not project_data:
            return json_error("not found project", 404)
        task = Task(data["title"], data["project_id"])
        db.add(task)
        db.commit()
        db.refresh(task)
        return json_ok(
            {"id": task.id, "title": task.title, "project_name": project_data.name}, 201
        )
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close()


@bp_tasks.route("/tasks", methods=["GET"])
def list_tasks():
    """
    list_tasks API
    """
    db = SessionLocal()
    try:
        tasks = db.query(Task).order_by(Task.id.desc()).all()
        task_list = []
        for task in tasks:
            project = db.get(Project, task.project_id)
            task_list.append(
                {"id": task.id, "title": task.title, "project_name": project.name}
            )
        return json_ok(task_list, 200)
    finally:
        db.close()


@bp_tasks.route("/tasks/{task_id}", methods=["GET"])
def get_task(task_id):
    """
    get_task by ID API
    """
    id = parse_int_param("task_id", task_id)
    if not isinstance(id, int):
        return id
    db = SessionLocal()
    try:
        task = db.get(Task, id)
        if not task:
            return json_error("not found", 404)
        project = db.get(Project, task.project_id)
        return json_ok(
            {
                "id": task.id,
                "title": task.title,
                "project_name": project.name if project else None,
            }
        )
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close()


@bp_tasks.route("/tasks/{task_id}", methods=["PATCH"])
def update_task(task_id):
    """
    update_task by ID API
    """
    id = parse_int_param("task_id", task_id)
    if not isinstance(id, int):
        return id
    data = validate_json(schema_update, bp_tasks.current_request)
    if not isinstance(data, dict):
        return data
    if not data:
        return json_error("no_fields_to_update", 400)
    db = SessionLocal()
    try:
        task = db.get(Task, id)
        if not task:
            return json_error("not found", 404)
        if "title" in data:
            task.title = data["title"]
        project = db.get(Project, task.project_id)
        db.add(task)
        db.commit()
        db.refresh(task)
        return json_ok(
            {
                "id": task.id,
                "title": task.title,
                "project_name": project.name if project else None,
            },
            200,
        )
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close()


@bp_tasks.route("/tasks/{task_id}", methods=["DELETE"])
def delete_task(task_id):
    """
    delete_task by ID API
    """
    id = parse_int_param("task_id", task_id)
    if not isinstance(id, int):
        return id
    db = SessionLocal()
    try:
        task = db.get(Task, id)
        if not task:
            return json_error("not found", 404)
        db.delete(task)
        db.commit()
        return json_ok({"oke": "task deleted successfully"}, 204)
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close()
