from chalice import Blueprint
from chalicelib.core.db import SessionLocal
from chalicelib.core.errors import json_error
from chalicelib.core.validators import validate_json, parse_int_param

from chalicelib.domain.models import User
from chalicelib.domain.schemas import UserCreateSchema, UserUpdateSchema

bp_users = Blueprint(__name__)
schema_create = UserCreateSchema()
schema_update = UserUpdateSchema()


@bp_users.route("/users", methods=["POST"])
def create_user():
    """
    create_user API
    """
    data = validate_json(schema_create, bp_users.current_request)
    if not isinstance(data, dict):
        return data
    db = SessionLocal()
    try:
        user = User(data["username"])
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"id": user.id, "username": user.username}
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close()


@bp_users.route("/users", methods=["GET"])
def list_users():
    """
    list_users GET API
    """
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.id.desc()).all()
        return [{"id": user.id, "username": user.username} for user in users]
    finally:
        db.close()


@bp_users.route("/users/{user_id}", methods=["GET"])
def get_user(user_id):
    """
    get_user by ID API
    """
    id = parse_int_param("user_id", user_id)
    if not isinstance(id, int):
        return id
    db = SessionLocal()
    try:
        user = db.get(User, id)
        if not user:
            return json_error("not_found", 404)
        return {"id": user.id, "username": user.username}
    finally:
        db.close()


@bp_users.route("/users/{user_id}", methods=["PATCH"])
def update_user(user_id):
    """
    update_user by id API
    """
    id = parse_int_param("user_id", user_id)
    if not isinstance(id, int):
        return id
    data = validate_json(schema_update, bp_users.current_request)
    if not isinstance(data, dict):
        return data
    if not data:
        return json_error("no_fields_to_update", 400)
    db = SessionLocal()
    try:
        user = db.get(User, id)
        if not user:
            return json_error("not found", 404)
        if "username" in data:
            user.username = data["username"]
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"id": user.id, "username": user.username}
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close()


@bp_users.route("/users/{user_id}", methods=["DELETE"])
def delete_user(user_id):
    """
    delete_user by id API
    """
    id = parse_int_param("user.id", user_id)
    if not isinstance(id, int):
        return id
    db = SessionLocal()
    try:
        user = db.get(User, id)
        if not user:
            return json_error("not found", 404)
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}, 204
    except Exception as e:
        db.rollback()
        return json_error(str(e), 500)
    finally:
        db.close()
