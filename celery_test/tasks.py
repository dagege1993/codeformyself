from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def send_email(email):
    print('send email to', email)
    import time
    time.sleep(5)
    return "success"
