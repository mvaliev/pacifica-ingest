#!/usr/bin/python
"""Celery utility functions."""
from __future__ import absolute_import, print_function
from time import sleep
import subprocess
from ingest.backend import tasks


def ping_celery():
    """Check to see if the celery process to bundle and upload is alive, alive."""
    ping_process = tasks.ping.delay()
    tries = 0
    while tries < 5:
        state = ping_process.state
        if state is not None:
            print(state)
            if state == 'PING' or state == 'SUCCESS':
                return True
        sleep(1)
        tries += 1
    return False


def start_celery():
    """Start the celery process."""
    alive = ping_celery()
    if not alive:
        try:
            print('attempting to start Celery')
            subprocess.Popen('celery -A UploadServer worker --loglevel=info', shell=True)
        # pylint: disable=broad-except
        except Exception as ex:
            print(ex)
        # pylint: enable=broad-except
    count = 0
    alive = False
    while not alive and count < 10:
        sleep(1)
        alive = ping_celery()
        count = count + 1
    return alive
