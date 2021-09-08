import joblib
import numpy as np
from celery import Celery


celery_app = Celery('tasks', backend='redis://redis', broker='redis://redis')
mdl = joblib.load('iris.mdl')


@celery_app.task(name='tasks.predict')
def predict(data):
    result = mdl.predict(np.array([data])).tolist()
    return result
