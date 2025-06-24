from airflow.models import DagRun, TaskInstance
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.db import provide_session
from airflow.utils.state import State
from flask import Blueprint, jsonify, render_template, url_for

calendar_bp = Blueprint(
    "all_status_view",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/all_status",
)


@calendar_bp.route("/api/failed_tasks/<dag_id>/<execution_date>")
@provide_session
def get_failed_tasks(dag_id, execution_date, session=None):
    from dateutil.parser import parse

    execution_date = parse(execution_date)
    tasks = (
        session.query(TaskInstance)
        .filter(
            TaskInstance.dag_id == dag_id,
            TaskInstance.execution_date == execution_date,
            TaskInstance.state == State.FAILED,
        )
        .all()
    )

    return jsonify([ti.task_id for ti in tasks])


@calendar_bp.route("/all_status")
@provide_session
def calendar_view(session=None):
    dag_runs = session.query(DagRun).filter(DagRun.state != State.REMOVED).all()

    # Build FullCalendar-compatible event objects
    events = []
    for run in dag_runs:
        events.append(
            {
                "title": f"{run.dag_id}",
                "start": run.execution_date.isoformat(),
                "end": run.execution_date.isoformat(),
                "url": url_for(
                    "Airflow.graph",
                    dag_id=run.dag_id,
                    execution_date=run.execution_date.isoformat(),
                ),
                "color": "#28a745"
                if run.state == State.SUCCESS
                else "#dc3545"
                if run.state == State.FAILED
                else "#ffc107",
            }
        )

    return render_template("calendar.html", events=events)


class CalendarViewPlugin(AirflowPlugin):
    name = "all_status_view_plugin"
    flask_blueprints = [calendar_bp]
