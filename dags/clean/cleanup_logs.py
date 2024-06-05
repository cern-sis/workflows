import os

import pendulum
from airflow.decorators import dag
from airflow.operators.bash import BashOperator

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")
LOG_DIR = "logs"
logs_dir = f"{AIRFLOW_HOME}/{LOG_DIR}"


@dag(start_date=pendulum.today("UTC").add(days=-1), schedule="@daily", catchup=False)
def cleanup_logs():
    BashOperator(
        task_id="cleanup_logs",
        bash_command=f"""
    logs_dir="{logs_dir}"
    find "$logs_dir" -type d -mtime +30 -exec rm -r {{}} \;
    """,
    )


cleanup_logs()
