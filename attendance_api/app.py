from chalice import Chalice
from chalicelib.core.db import engine
from chalicelib.domain.models import Base
from chalicelib.api.blueprints import bp_projects, bp_tasks, bp_users

app = Chalice(app_name="attendance_api")
Base.metadata.create_all(bind=engine)

app.register_blueprint(bp_projects)
app.register_blueprint(bp_tasks)
app.register_blueprint(bp_users)


@app.route("/")
def index():
    """test db"""
    return {"status": "oke"}
