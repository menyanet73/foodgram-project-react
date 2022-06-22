# FOODGRAM: Service for your recipes

Service with registration, following, and food recipes sharing.
Can compose shopping list, with necessary ingredients, for simple shopping.

Project aviable in http://62.84.120.58


#### Stack: 
Python 3, Django, gunicorn, PostgreSQL, nginx, react

## How start project:

Clone a repository and go to command line:

```sh
git clone https://github.com/menyanet73/foodgram-project-react.git
```

```sh
cd foodgram-project-react/
```

Create .env file.

```sh
touch .env
```

Fill it in with your data. 

```sh
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
DB_HOST='db'
DB_PORT='5432'
SECRET_KEY='djangosecretkey'
ALLOWED_HOSTS=['your_ip', 'localhost']
```

```sh
cd infra
```

Create/download docker-compose images and containers

```sh
docker-compose up
```


Done!


### Author
##### https://github.com/menyanet73
### Frontend
#### YANDEX PRACTICUM