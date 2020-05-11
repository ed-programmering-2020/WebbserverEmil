# Webbserver

*Alla kommandon behövs köras inuti projektets mapp*

<br/>

## Setup

### 1. Ladda ner Python

Den senaste versionen kan laddas ner från <a href="https://www.python.org/downloads/">www.python.org</a>

Välj **Add Python3.x to Path**.

<br/>

### 2. Installera alla nödvändiga bibliotek

Använd detta kommandot:
```
pip install -r requirements.txt
```

<br/>

### 3. Sätta upp databasen

Använd detta kommandot:
```
python manage.py init
python manage.py makemigrations
python manage.py migrate
```

<br/>

### 4. Skapa admin användare
För att skapa en användare som har tillgång till admin konsolen (databas gränssnittet) behövs detta kommandot köras:
```
python manage.py createsuperuser
```

<br/>

## Start

Starta webbservern med kommandot:
```
python manage.py runserver
```

*Om admin konsolen (databas gränssnittet) är av intresse finns den på http://127.0.0.1:8000/admin/*









