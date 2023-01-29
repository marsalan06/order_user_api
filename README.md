# order_api_django
Order and User API interaction

This is a set of API with authentication and their operations with a model named Order.

Documentation of API can be found at https://documenter.getpostman.com/view/10266866/2s935hPmmY

Steps to run the django project locally
--> mkdir directory
--> cd directory
--> python -m venv venv
--> source venv/bin/activate
--> pip install -r requirements.txt
--> python manage.py runserver


steps to run docker container
--> docker build -t django-sales-project .
--> docker run -it -p 8000:8000 django-sales-project
