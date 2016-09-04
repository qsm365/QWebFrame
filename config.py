# -*- coding:utf-8 -*-

SQLALCHEMY_DATABASE_URI = 'mysql://testuser:asdf1234@192.168.3.13:3306/testuser'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SESSION_STORE_TYPE = 'cookie'
#SESSION_STORE_TYPE = 'token'

SESSION_TYPE = 'filesystem'
SECRET_KEY = 'SECRET_KEY'

TIMEZONE = 'Asia/Shanghai'

CELERY_BROKER_URL = 'redis://192.168.3.13:6379'
#CELERY_RESULT_BACKEND = 'redis://192.168.3.13:6379'
#CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_RESULT_BACKEND = 'db+mysql://testuser:asdf1234@192.168.3.13:3306/testuser'
CELERY_RESULT_DB_TABLENAMES = {
    'task': 'celery_taskmeta',
    'group': 'celery_tasksetmeta',
}
CELERY_TIMEZONE = TIMEZONE
CELERY_ACCEPT_CONTENT = ['pickle']
