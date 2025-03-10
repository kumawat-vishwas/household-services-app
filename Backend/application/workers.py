from celery import Celery
from flask import current_app as app


celery = Celery("Application Jobs")
celery.conf.enable_utc = False
celery.conf.timezone = "Asia/Calcutta"
class ContextTask(celery.Task):
    def __call__(self,*args,**kwargs):
        with app.app_context():
            return self.run(*args,**kwargs)

from celery import Celery
from flask import current_app as app


celery = Celery("Application Jobs")
celery.conf.enable_utc = False
celery.conf.timezone = "Asia/Calcutta"
class ContextTask(celery.Task):
    def __call__(self,*args,**kwargs):
        with app.app_context():
            return self.run(*args,**kwargs)

