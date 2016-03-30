"""
Module that contains all the amqp tasks that support the
ingest infrastructure
"""

from __future__ import absolute_import
import os
import datetime
import pycurl
from peewee import DoesNotExist
from celery import shared_task, current_task
from .celery import INGEST_APP

#@INGEST_APP.task(ignore_result=False)

@INGEST_APP.task(ignore_result=False)
def thingy():
    """ thingy """
    print 'thingy'

@INGEST_APP.task(ignore_result=False)
def ping():
    """
    check to see if the celery task process is started.
    """
    print 'Pinged!'

    current_task.update_state(state='PING', meta={'Status': "Background process is alive"})

    print 'updated ping status'

