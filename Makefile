install:
	poetry install

db_init:
	poetry run flask --app task_manager/app:app db init

db_migrate:
	poetry run flask --app task_manager/app:app db migrate -m "create tables"

db_upgrade:
	poetry run flask --app task_manager/app:app db upgrade

dev:
	poetry run flask --app task_manager/app:app --debug run
