from marshmallow import ValidationError
from chalicelib.core.errors import json_error


def validate_json(schema, request):
    """
    Validate JSON body cho POST/PATCH/PUT
    - schema: instance schema (vd UserCreateSchema())
    - request: current_request
    Trả về: dict data đã validate
    Nếu lỗi: trả Response 422 (json_error)
    """

    payload = request.json_body
    if payload is None:
        return json_error("json_body_required", 400)
    try:
        return schema.load(payload)
    except ValidationError as ve:
        return json_error("validation_error", 422, ve.messages)


def validate_query(schema, request):
    """
    Validate query params cho GET.
    Chalice query_params có thể None
    """
    query_params = request.query_params or {}
    try:
        return schema.load(query_params)
    except ValidationError as ve:
        return json_error("validation_error", 422, ve.messages)


def parse_int_param(name: str, value: str):
    """
    Validate path param kiểu int, ví dụ user_id.
    - name: tên param (để báo lỗi)
    - value: string nhận từ URL
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return json_error(f"invalid_{name}", 422, {name: ["must be interger"]})
