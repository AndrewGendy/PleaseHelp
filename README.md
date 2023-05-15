Project Setup
==============

Project setup instructions here.

1.0 install git

1.1 install poetry (this will install python, django, and everything else)
    1.1.1 configure it to use in-project venv using this command: "poetry config virtualenvs.in-project true"
    1.1.2 install all packages needed for the project using this command: "poetry install"
    1.1.3 use "poetry run" before using any python command, for example: "poetry run python manage.py runserver"