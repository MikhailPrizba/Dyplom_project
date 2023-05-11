FORMAT_FOLDER?=farmer





black:
	python3 -m black ${FORMAT_FOLDER}
isort:
	python3 -m isort ${FORMAT_FOLDER}
flake8:
	python3 -m flake8 ${FORMAT_FOLDER}
interrogate:
	python3 -m interrogate ${FORMAT_FOLDER}

format:
	make black 
	make isort 
	make flake8 
	make interrogate 

start:
	pip install -r requirements.txt
	python3 ${FORMAT_FOLDER}/manage.py makemigrations
	python3 ${FORMAT_FOLDER}/manage.py migrate

runserver:
	python3 ${FORMAT_FOLDER}/manage.py runserver