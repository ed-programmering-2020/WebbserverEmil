# Orpose-Backend

This is the backend section of the service Orpose which is a website that matches users with products based on their preferences.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python3 is required as that is the language used. The requirements.txt lists all requirements relating to python. 


### Installing

To get the project up and running on a local system, you need prepare the database.

Initialize the database with
```
python manage.py init
```

And then to set up all models in the project use
```
python manage.py makemigrations
python manage.py migrate
```
