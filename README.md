# Webbserver - slutprojekt

*Alla kommandon behövs köras i projektets mapp*

## Setup

### 1. Ladda ner Python

Programmeringsspråket som används är Python3 vilket kan laddas ner från https://www.python.org/downloads/


### 2. Installera bibliotek

För att sedan installera alla bibliotek som används i projektet behövs detta kommmandot köras:
```
pip install -r requirements.txt
```

### 3. Sätta upp databasen

För att sätta upp den lokala databasen behövs dessa kommandon köras:
```
python manage.py init
python manage.py makemigrations
python manage.py migrate
```

### 4. Skapa admin användare
För att skapa en användare som har tillgång till admin konsolen (databas gränssnittet) behövs detta kommandot köras:
```
python manage.py createsuperuser
```

## Start

Starta webbservern med kommandot:
```
python manage.py runserver
```

*Om admin konsolen (databas gränssnittet) är av intresse finns den på http://127.0.0.1:8000/admin/*









