# Webbserver - slutprojekt

*Alla kommandon behövs köras inuti projektets mapp*

## Setup

### 1. Ladda ner Python

Programmeringsspråket kan laddas ner från https://www.python.org/downloads/ (välj senaste version).

Under installationen måste **Add Python3.x to Path** fyllas i.


### 2. Installera alla nödvändiga bibliotek

Använd detta kommandot:
```
pip install -r requirements.txt
```


### 3. Sätta upp databasen

Använd detta kommandot:
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









