"""
Module that contains all the amqp tasks that support the
ingest infrastructure
"""

from __future__ import absolute_import

from celery import current_task
from .celery import INGEST_APP

from time import sleep

from ingest_orm import update_state

@INGEST_APP.task(ignore_result=False)
def ingest(job_id, filepath):
    """
    ingest a tar bundle into the archive
    """

    for i in range(1, 10):
        sleep(1)
        print i*10
        update_state(job_id, 'Super OK', 'Ingesting ' + filepath, i*10)





@INGEST_APP.task(ignore_result=False)
def ping():
    """
    check to see if the celery task process is started.
    """
    print 'Pinged!'

    current_task.update_state(state='PING', meta={'Status': "Background process is alive"})

    print 'updated ping status'

