# Webbserver

*Alla kommandon behövs köras inuti projektets mapp*


### Python installation

Den senaste versionen av programmeringsspråket kan laddas ner från <a href="https://www.python.org/downloads/">www.python.org</a>

Vid installation:
Välj **Add Python3.x to Path**.

För att installera alla nödvändiga bibliotek:
```
pip install -r requirements.txt
```


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

### Starta webbserver

```
python manage.py runserver
```

Admin konsolen finns på http://127.0.0.1:8000/admin/









