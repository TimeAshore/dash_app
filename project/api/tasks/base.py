# services/socamas/project/api/tasks/base.py
from celery import Celery
from project.config import DevelopmentConfig

socweb = Celery('socweb_gov', backend=DevelopmentConfig.MESSAGE_QUEUE, broker=DevelopmentConfig.MESSAGE_QUEUE,
                include=['project.api.tasks.celery'])
