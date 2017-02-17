#!/usr/bin/python
"""Module that contains all the amqp tasks that support the ingest infrastructure."""
from __future__ import absolute_import, print_function
# from time import sleep
import os
import requests
# from ingest.orm import IngestState, BaseModel, update_state, read_state
# from ingest.utils import get_job_id
# from ingest import tarutils
from ingest.tarutils import open_tar
from ingest.tarutils import MetaParser
from ingest.tarutils import TarIngester
from ingest.orm import update_state
from celery import current_task
from .celery_ingest import INGEST_APP


@INGEST_APP.task(ignore_result=False)
def ingest(job_id, filepath):
    """Ingest a tar bundle into the archive."""
    update_state(job_id, 'OK', 'Open tar', 0)
    tar = open_tar(filepath)
    update_state(job_id, 'OK', 'Open tar', 100)

    update_state(job_id, 'OK', 'load metadata', 0)
    meta = MetaParser()
    meta.load_meta(tar, job_id)
    update_state(job_id, 'OK', 'load metadata', 100)

    ingest_obj = TarIngester(tar, meta)

    # validate policy
    success = validate_meta(meta.meta_str)
    if not success:
        update_state(job_id, 'FAILED', 'Policy Validation', 0)
        return
    update_state(job_id, 'OK', 'Policy Validation', 100)

    update_state(job_id, 'OK', 'ingest files', 0)
    success = ingest_obj.ingest()
    if not success:
        # rollback files
        update_state(job_id, 'FAILED', 'ingest files', 0)
        return
    update_state(job_id, 'OK', 'ingest files', 100)

    update_state(job_id, 'OK', 'ingest metadata', 0)
    success = meta.post_metadata()
    if not success:
        # rollback files
        update_state(job_id, 'FAILED', 'ingest metadata', 0)
        return
    update_state(job_id, 'OK', 'ingest metadata', 100)


def validate_meta(meta_str):
    """Validate metadata."""
    try:
        archivei_server = os.getenv('POLICY_SERVER', '127.0.0.1')
        archivei_port = os.getenv('POLICY_PORT', '8181')
        archivei_url = 'http://{0}:{1}/ingest'.format(archivei_server, archivei_port)

        headers = {'content-type': 'application/json'}

        req = requests.post(archivei_url, headers=headers, data=meta_str)

        try:
            if req.json()['status'] == 'success':
                return True
        # pylint: disable=broad-except
        except Exception:
            print (req.content)
            return False
        # pylint: enable=broad-except
    # pylint: disable=broad-except
    except Exception:
        return False
    # pylint: enable=broad-except


@INGEST_APP.task(ignore_result=False)
def ping():
    """Check to see if the celery task process is started."""
    print('Pinged!')
    current_task.update_state(state='PING', meta={'Status': 'Background process is alive'})
    print('updated ping status')
