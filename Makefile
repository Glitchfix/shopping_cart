install-deps:
	pip install -r requirements.txt
test:
	python manage.py test
makemigrations:
	python manage.py makemigrations
migrate:
	python manage.py migrate
cleanup-db:
	rm -rf db.sqlite3
run:
	python3 manage.py runserver

reset-run: makemigrations migrate run
