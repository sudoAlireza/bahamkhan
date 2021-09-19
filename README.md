# Bahamkhan

### A platform for finding study partners or create and find study groups

![GitHub Logo](/static/img/alumni.png)

# Installation

clone:
```
git clone https://github.com/alireza-f/bahamkhan.git
```

Go to dir:
```
cd bahamkhan
```

install requieremts
```
pip3 install requirements.txt
```


# Create Docker Image

create yml file:
```
touch docker-compose.yml
```
write your yml file like this:
```
version: '3.8'

services:
  web:
    build: .
    command: python bahamkhan/manage.py runserver 0.0.0.0:8000
    environment: 
      - SECRET_KEY=your_secret_key
    volumes:
      - .:/bahamkhan
    ports:
      - 8000:8000
    depends_on:
      - db
    links:
      - db:db

  db:
    image: postgres:11
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - '5432'
    environment:
      - POSTGRES_DB=postgresql
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

volumes:
  postgres_data:

```

# Check django DEBUG Mood

check settings.py file, Debug should be True

```
DEBUG = False
```

# Run
```
 docker build . 
 docker up -d --build
 docker-compose exec web python manage.py makemigrations
 docker-compose exec web python manage.py migrate
 docker-compose exec web python manage.py createsuperuser
```

# I Will Be Happy:
Star the project, fork and contribute.
thanks.
