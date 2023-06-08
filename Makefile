export PYTHON_VERSION = 3.10.11


WEBSERVER_PID=airflow-webserver-monitor.pid
TRIGGERER_PID=airflow-triggerer.pid
SCHEDULER_PID=airflow-scheduler.pid
WORKER_PID=airflow-worker.pid
FLOWER_PID=airflow-flower.pid

init:
	pyenv global $(PYTHON_VERSION)
	pyenv install ${PYTHON_VERSION}
	pyenv virtualenv ${PYTHON_VERSION} workflows
	pyenv activate workflows
	export AIRFLOW_HOME=${PWD}

start: compose sleep airflow create_ftp

sleep:
	sleep 10

buckets:
	docker-compose up -d create_buckets

airflow:
	airflow db init
	airflow webserver -D
	airflow triggerer -D
	airflow scheduler -D
	airflow celery worker -D
	airflow celery flower -D
	echo -e "\033[0;32m Airflow Started. \033[0m"

create_ftp:
	airflow connections add 'oup_ftp_service' --conn-json '{"conn_type": "ftp","login": "airflow","password": "airflow", "host": "127.0.0.1", "port": 40009}'


compose:
	docker-compose up -d redis postgres sftp ftp s3 create_buckets
	sleep 5

stop:
	docker-compose down
	kill -9 $(lsof -ti:8080)
	kill -9 $(lsof -ti:5555)
	kill -9 $(lsof -ti:8793)
	rm *.out *.err
	echo -e "\033[0;32m Airflow Stoped. \033[0m"
