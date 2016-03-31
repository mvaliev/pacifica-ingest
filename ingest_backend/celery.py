#pylint: disable=no-member
#pylint: disable=invalid-name
#justification: because pylint doesn't get celery

"""
Primary celery process.
"""
from __future__ import absolute_import
from celery import Celery
import settings


INGEST_APP = Celery('ingest_backend',
                    broker=settings.BROKER_URL,
                    backend="amqp",
                    include=['ingest_backend.tasks'])

INGEST_APP.config_from_object('settings')

# Optional configuration, see the application user guide.
INGEST_APP.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    INGEST_APP.start()
