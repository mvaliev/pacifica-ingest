#!/usr/bin/python
"""Test ingest."""
from __future__ import print_function
from subprocess import call
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


def test_bad_upload():
    """Test the upload."""
    with open('test_data/bad-proposal.tar', 'rb') as filefd:
        req = requests.post(
            'http://127.0.0.1:8066/upload',
            data=filefd,
            headers={
                'Content-Type': 'application/octet-stream'
            }
        )
        assert req.status_code == 200
        job_state = check_upload_state(loads(req.text)['job_id'])
        try_assert_job_state(job_state, 'FAILED', 'Policy Validation', 0)


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


def test_good_upload():
    """Test the good upload."""
    try_good_upload('good', 'OK', 'ingest metadata', 100)


def test_bad_archiveinterface_upload():
    """Test if the archive interface is down."""
    call(['docker-compose', 'stop', 'archiveinterface'])
    try_good_upload('good', 'FAILED', 'ingest files', 0)
    call(['docker-compose', 'start', 'archiveinterface'])


def test_bad_policy_upload():
    """Test if the archive interface is down."""
    call(['docker-compose', 'stop', 'policyserver'])
    try_good_upload('good', 'FAILED', 'Policy Validation', 0)
    call(['docker-compose', 'start', 'policyserver'])
    sleep(2)


def test_bad_hashsum_upload():
    """Test if the metadata is down."""
    try_good_upload('bad-hashsum', 'FAILED', 'ingest files', 0)


def test_bad_metadata_upload():
    """Test if the metadata is down."""
    try_good_upload('bad-mimetype', 'FAILED', 'ingest metadata', 0)


def test_bad_tarfile_upload():
    """Test if the metadata is down."""
    try_good_upload('bad-tarfile', 'FAILED', 'Bad tarfile', 0)
