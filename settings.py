"""
    Celery settings
"""

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'amqp'

CELERYD_STATE_DB = "celery_worker_state"

CELERY_DISABLE_RATE_LIMITS = True

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_IGNORE_RESULT = False
