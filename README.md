# Webbserver

*Alla kommandon behöver köras inuti projekt mappen*

<br/>

### Python installation

Den senaste versionen av programmeringsspråket kan laddas ner från <a href="https://www.python.org/downloads/">www.python.org</a>

Vid installation välj **Add Python3.x to Path**.

För att installera alla nödvändiga bibliotek:
```
pip install -r requirements.txt
```

<br/>

### Skapa lokal databas
```
python manage.py init
python manage.py makemigrations
python manage.py migrate
```

För att skapa en admin användare:
```
python manage.py createsuperuser
```

<br/>

### Starta webbserver

```
python manage.py runserver
```

Admin konsolen finns på http://127.0.0.1:8000/admin/









