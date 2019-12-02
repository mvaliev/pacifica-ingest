#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test module for the ingest python code."""
from os.path import join
from time import sleep
from json import loads
import tarfile
import requests


def check_upload_state(job_id, wait):
    """Get the upload state and return results."""
    sleep(wait)
    req = requests.get(
        'http://127.0.0.1:8066/get_state?job_id={}'.format(job_id))
    assert req.status_code == 200
    job_state = loads(req.text)
    return job_state


def try_assert_job_state(job_state, state, task, percent):
    """assert on the job state bits."""
    assert job_state['state'] == state
    assert job_state['task'] == task
    assert int(float(job_state['task_percent'])) == percent


def try_good_move(mdfile, state, task, percent, wait=5):
    """Test the move and see if the state task and percent match."""
    with open(join('test_data', '{}.json'.format(mdfile)), 'r') as filefd:
        req = requests.post(
            'http://127.0.0.1:8066/move',
            data=filefd.read(),
            headers={'content-type': 'application/json'}
        )
        assert req.status_code == 200
        job_id = req.json()['job_id']
        job_state = check_upload_state(job_id, wait)
        try_assert_job_state(job_state, state, task, percent)


def try_good_upload(tarfile, state, task, percent, wait=5):
    """Test the upload and see if the state task and percent match."""
    with open(join('test_data', '{}.tar'.format(tarfile)), 'rb') as filefd:
        req = requests.post(
            'http://127.0.0.1:8066/upload',
            data=filefd,
            headers={
                'Content-Type': 'application/octet-stream'
            }
        )
        assert req.status_code == 200
        job_state = check_upload_state(loads(req.text)['job_id'], wait)
        try_assert_job_state(job_state, state, task, percent)


def try_good_upload1(bundle_name, state, task, percent, wait=5):
    """Test the upload and see if the state task and percent match."""
    tar = tarfile.open(bundle_name)
    for tarinfo in tar:
        print(tarinfo.name, "is", tarinfo.size, "bytes in size and is", end="")
        if tarinfo.isreg():
            print("a regular file.")
        elif tarinfo.isdir():
            print("a directory.")
        else:
            print("something else.")
    tar.close()

    with open(bundle_name, 'rb') as filefd:
        req = requests.post(
            'http://127.0.0.1:8066/upload',
            data=filefd,
            headers={
                'Content-Type': 'application/octet-stream'
            }
        )
        assert req.status_code == 200
        job_state = check_upload_state(loads(req.text)['job_id'], wait)
        try_assert_job_state(job_state, state, task, percent)
