"""
"""
from __future__ import absolute_import



def start_celery():
    """
    starts the celery process
    """

    alive = ping_celery()
    if not alive:
        try:
            print 'attempting to start Celery'
            subprocess.Popen('celery -A UploadServer worker --loglevel=info', shell=True)
        except Exception, e:
            print e

    count = 0
    alive = False
    while not alive and count < 10:
        sleep(1)
        alive = ping_celery()
        count = count + 1

    return alive