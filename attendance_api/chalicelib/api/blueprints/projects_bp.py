from chalice import Blueprint
from chalicelib.core.db import SessionLocal
from chalicelib.core import json_error, json_ok
from chalicelib.core.validators import validate_json, parse_int_param
from chalicelib.domain.models import Project, User
from chalicelib.domain.schemas import ProjectCreateSchema, ProjectUpdateSchema

bp_projects = Blueprint(__name__)
schema_create = ProjectCreateSchema()
schema_update = ProjectUpdateSchema()


@bp_projects.route("/projects", methods=["POST"])
def create_project():
    """
    create_project の API
    """
    data = validate_json(schema_create, bp_projects.current_request)
    if not isinstance(data, dict):
        return data
    db = SessionLocal()
    try:
        user_data = db.get(User, data["owner_id"])
        if not user_data:
            return json_error("not found user", 404)
        project = Project(data["name"], data["owner_id"])
        db.add(project)
        db.commit()
        db.refresh(project)
        return json_ok(
            {
                "id": project.id,
                "project_name": project.name,
                "username": user_data.username,
            },
            201,
        )
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close


@bp_projects.route("/projects", methods=["GET"])
def list_project():
    """
    list_project の API
    """
    db = SessionLocal()
    try:
        projects = db.query(Project).order_by(Project.id.desc()).all()
        project_list = []
        for project in projects:
            user = db.get(User, project.owner_id)
            project_list.append(
                {
                    "id": project.id,
                    "project_name": project.name,
                    "username": user.username if user else None,
                }
            )
        return json_ok(project_list, 200)
    finally:
        db.close()


@bp_projects.route("/projects/{project_id}", methods=["GET"])
def get_project(project_id):
    """
    get_project by id API
    """
    id = parse_int_param("project_id", project_id)
    if not isinstance(id, int):
        return id
    db = SessionLocal()
    try:
        project = db.get(Project, id)
        if not project:
            return json_error("not found", 404)
        user = db.get(User, project.owner_id)
        return json_ok(
            {
                "id": project.id,
                "name": project.name,
                "username": user.username if user else None,
            }
        )
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close()


@bp_projects.route("/projects/{project_id}", methods=["PATCH"])
def update_project(project_id):
    """
    update_project by id API
    """
    id = parse_int_param("project_id", project_id)
    if not isinstance(id, int):
        return id
    data = validate_json(schema_update, bp_projects.current_request)
    if not isinstance(data, dict):
        return data
    if not data:
        return json_error("no_fields_to_update", 400)
    db = SessionLocal()
    try:
        project = db.get(Project, id)
        if not project:
            return json_error("not found", 404)
        if "name" in data:
            project.name = data["name"]
        user = db.get(User, project.owner_id)
        db.add(project)
        db.commit()
        db.refresh(project)
        return json_ok(
            {
                "id": project.id,
                "project_name": project.name,
                "username": user.username if user else None,
            },
            200,
        )
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close()


@bp_projects.route("/projects/{project_id}", methods=["DELETE"])
def delete_project(project_id):
    """
    delete_project by ID API
    """
    id = parse_int_param("project_id", project_id)
    if not isinstance(id, int):
        return id
    db = SessionLocal()
    try:
        project = db.get(Project, id)
        if not project:
            return json_error("not found", 404)
        db.delete(project)
        db.commit()
        return json_ok({"oke": "project deleted successfully"}, 204)
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close()
