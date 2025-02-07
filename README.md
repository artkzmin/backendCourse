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