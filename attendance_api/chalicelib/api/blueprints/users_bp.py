from chalice import Blueprint
from chalicelib.core.db import SessionLocal
from chalicelib.core.errors import json_error
from chalicelib.core.validators import validate_json, parse_int_param

from chalicelib.models import User
from chalicelib.schemas.u