export PYTHON_VERSION = 3.8.13


WEBSERVER_PID=airflow-webserver.pid
TRIGGERER_PID=airflow-triggerer.pid
SCHEDULER_PID=airflow-scheduler.pid

init:
	pyenv global $(PYTHON_VERSION)
	pyenv install ${PYTHON_VERSION}
	pyenv virtualenv ${PYTHON_VERSION} workflows
	pyenv activate workflows
	export AIRFLOW_HOME=${PWD}
	
start:
	docker-compose up -d redis postgres sftp
	airflow webserver -D
	airflow triggerer -D
	airflow scheduler -D
	echo -e "\033[0;32m Airflow Started. \033[0m"

stop:
	docker-compose down
	cat $(WEBSERVER_PID) | xargs kill
	cat $(TRIGGERER_PID) | xargs kill
	cat $(SCHEDULER_PID) | xargs kill
	rm *.out *.err
	echo -e "\033[0;32m Airflow Stoped. \033[0m"
