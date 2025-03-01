## Celery

### Запуск worker
```
celery -A src.tasks.celery_app:celery_instance worker --pool=solo
```

### Запуск celery-worker -l INFO
```
celery -A src.tasks.celery_app:celery_instance worker -l INFO --pool=solo
```

### Запуск celery-beat
```
celery -A src.tasks.celery_app:celery_instance beat -l INFO
```


## Pytest

### Запуск тестирования
```
pytest -v
```
Запуск тестирования с дебагом
```
pytest -v -s
```

## Docker

### Создание сети
```
docker network create myNetwork
```

### Запуск БД
```
sudo docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcdeuinrmv0u3894ut289v30yt978f34hk297t \
    -e POSTGRES_DB=booking
    --network=myNetwork \
    --volume pg-booking-data:/var/lig/postgresql/data \
    -d postgres:16
```
В одну строку:
```
sudo docker run --name booking_db -p 6432:5432 -e POSTGRES_USER=abcde -e POSTGRES_PASSWORD=abcdeuinrmv0u3894ut289v30yt978f34hk297t -e POSTGRES_DB=booking --network=myNetwork --volume pg-booking-data:/var/lig/postgresql/data -d postgres:16
```

### Запуск Redis
```
sudo docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4
```
В одну строку:
```
sudo docker run --name booking_cache -p 7379:6379 --network=myNetwork -d redis:7.4
```

### Запуск Nginx
```
sudo docker run --name booking_nginx \
    --volume=./nginx.conf:/etc/nginx/nginx.conf \
    --volume=/etc/letsencrypt:/etc/letsencrypt \
    --volume=/var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=myNetwork \
    --rm -p 443:443 nginx
```
В одну строку:
```
sudo docker run --name booking_nginx --volume=./nginx.conf:/etc/nginx/nginx.conf --volume=/etc/letsencrypt:/etc/letsencrypt --volume=/var/lib/letsencrypt:/var/lib/letsencrypt --network=myNetwork --rm -p 443:443 nginx
```

### Сборка Backend
```
docker build -t booking_image .
```
Без использования кэша:
```
docker build --no-cache -t booking_image .
```
### Запуск Backend
```
docker run --name booking_back \
    -p 7777:8000 \
    --network=myNetwork \
    booking_image
```
В одну строку:
```
docker run --name booking_back -p 7777:8000 --network=myNetwork booking_image
```

### Запуск Celery
#### Worker
```
docker run --name booking_celery_worker \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO
```
В одну строку:
```
docker run --name booking_celery_worker --network=myNetwork booking_image celery --app=src.tasks.celery_app:celery_instance worker -l INFO
```

#### Beat
```
docker run --name booking_celery_beat \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance beat -l INFO
```
В одну строку:
```
docker run --name booking_celery_beat --network=myNetwork booking_image celery --app=src.tasks.celery_app:celery_instance beat -l INFO
```






# GitLab CI

https://github.com/artemonsh/backend-course/blob/main/docs/gitlab-runner.md

## Запуск раннера
```
sudo docker run -d --name gitlab-runner --restart always \
  --dns 8.8.8.8 --dns 8.8.4.4 \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:alpine
```

## Регистрация раннера
```
sudo docker run --rm -it \
  --dns 8.8.8.8 --dns 8.8.4.4 \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  gitlab/gitlab-runner:alpine register
```