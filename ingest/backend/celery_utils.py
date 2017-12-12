#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Celery utility functions."""
from __future__ import absolute_import, print_function
from time import sleep
from ingest.backend import tasks


# this is a developer testing utility used to test connectivity
def ping_celery():  # pragme: no cover
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
