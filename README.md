# Webbserver

*Alla kommandon behövs köras inuti projektets mapp*

Admin konsolen finns på http://127.0.0.1:8000/admin/


### Setup

#### 1. Ladda ner Python

Den senaste versionen kan laddas ner från <a href="https://www.python.org/downloads/">www.python.org</a>

Välj **Add Python3.x to Path**.


#### 2. Installera alla nödvändiga bibliotek

*Använd detta kommandot:*
```
pip install -r requirements.txt
```


#### 3. Sätta upp databasen

*Använd dessa kommandon:*
```
python manage.py init
python manage.py makemigrations
python manage.py migrate
```


#### 4. Skapa admin användare

*Använd detta kommandot:*
```
python manage.py createsuperuser
```

### Start

Starta webbservern med kommandot:
```
python manage.py runserver
```









