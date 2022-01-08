from celery import shared_task

@shared_task(queue='ulala')
def ulala():
    print('ulalal')
    return " hola"

@shared_task
def add(x, y):
    return x + y