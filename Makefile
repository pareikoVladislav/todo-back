migrate:
	python manage.py makemigrations
	python manage.py migrate

createuser:
	python manage.py createsuperuser

run:
	python manage.py runserver

shell:
	python manage.py shell

test:
	python manage.py test
