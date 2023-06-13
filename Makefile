export AIRFLOW_HOME=${PWD}
export PYTHON_VERSION = 3.10.11

FLOWER_PID=airflow-flower.pid
SCHEDULER_PID=airflow-scheduler.pid
TRIGGERER_PID=airflow-triggerer.pid
WEBSERVER_MONITOR_PID=airflow-webserver-monitor.pid
WEBSERVER_PID=airflow-webserver.pid
WORKER_PID=airflow-worker.pid

init:
	pyenv global $(PYTHON_VERSION)
	pyenv install ${PYTHON_VERSION}
	pyenv virtualenv ${PYTHON_VERSION} workflows
	pyenv activate workflows

start: compose sleep airflow create_ftp

sleep:
	sleep 5

buckets:
	docker-compose up -d create_buckets

airflow:
	echo -e "\033[0;32m Starting Airflow with ${AIRFLOW_HOME} \033[0m"
	airflow db init
	airflow users create \
		--username admin \
		--password admin \
		--role Admin \
		--firstname FIRST_NAME \
		--lastname LAST_NAME \
		--email admin@worfklows.cern
	airflow webserver -D
	airflow triggerer -D
	airflow scheduler -D
	airflow celery worker -D
	airflow celery flower -D
	echo -e "\033[0;32m Airflow Started. \033[0m"

create_ftp:
	-airflow connections add 'oup_ftp_service' --conn-json '{"conn_type": "ftp","login": "airflow","password": "airflow", "host": "127.0.0.1", "port": 21}'

compose:
	docker-compose up -d redis postgres sftp ftp s3 create_buckets

stop:
	docker-compose down
	-kill -9 $(lsof -ti:8080)
	-kill -9 $(lsof -ti:5555)
	-kill -9 $(lsof -ti:8793)
	-cat $(WEBSERVER_PID) | xargs kill  -9
	-cat $(TRIGGERER_PID) | xargs kill -9
	-cat $(SCHEDULER_PID) | xargs kill -9
	-cat $(WORKER_PID) | xargs kill -9
	-cat $(FLOWER_PID) | xargs kill -9
	-cat $(WEBSERVER_MONITOR_PID) | xargs kill -9
	-rm *.out *.err *.pid *.log
	-kill -9 $(lsof -ti:8080)
	-kill -9 $(lsof -ti:5555)
	-kill -9 $(lsof -ti:8793)
	echo -e "\033[0;32m Airflow Stoped. \033[0m"
