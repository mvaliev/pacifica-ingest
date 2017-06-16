#!/usr/bin/python
"""Test module for the ingest python code."""
from time import sleep
from json import loads
import requests


def check_upload_state(job_id):
    """Get the upload state and return results."""
    sleep(3)
    req = requests.get('http://127.0.0.1:8066/get_state?job_id={}'.format(job_id))
    assert req.status_code == 200
    job_state = loads(req.text)
    return job_state


def try_assert_job_state(job_state, state, task, percent):
    """assert on the job state bits."""
    assert job_state['state'] == state
    assert job_state['task'] == task
    assert int(float(job_state['task_percent'])) == percent


def try_good_upload(tarfile, state, task, percent):
    """Test the upload and see if the state task and percent match."""
    with open('test_data/{}.tar'.format(tarfile), 'rb') as filefd:
        req = requests.post(
            'http://127.0.0.1:8066/upload',
            data=filefd,
            headers={
                'Content-Type': 'application/octet-stream'
            }
        )
        assert req.status_code == 200
        job_state = check_upload_state(loads(req.text)['job_id'])
        try_assert_job_state(job_state, state, task, percent)
