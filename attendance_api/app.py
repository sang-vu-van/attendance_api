from chalice import Chalice
from chalicelib.core.db import engine
from chalicelib.models import Base

app = Chalice(app_name="attendance_api")
Base.metadata.create_all(bind=engine)


@app.route("/")
def index():
    """test db"""
    return {"status": "oke"}
