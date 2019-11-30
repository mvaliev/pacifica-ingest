#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test ingest with good uploads of good and bad data."""
from __future__ import print_function, absolute_import
import requests
from common_methods_test import try_good_upload, try_good_upload1
from make_data_test import make_data
from contextlib import contextmanager
import tarfile
from os.path import join, dirname, abspath
from os import remove
from shutil import copy, Error

_THIS_DIR = dirname(abspath(__file__))
_DATA_DIR = join(_THIS_DIR, 'test_data')
_META_DATA_DIR = join(_DATA_DIR, 'metadata-files')


@contextmanager
def test_data(prefix, custom_meta_file=None):
    """generate data for tests."""
    if custom_meta_file:
        meta_file_in = join(_META_DATA_DIR, custom_meta_file)
    else:
        meta_file_in = join(_META_DATA_DIR, '%s-md.json' % prefix)
    meta_file = join(_DATA_DIR, 'metadata.txt')
    tar_file_out = join(_DATA_DIR, '%s.tar' % prefix)
    data_dir = join(_DATA_DIR, 'data')

    try:
        copy(meta_file_in, meta_file)
    except Error:
        print('problems copying metafile')
        raise

    with tarfile.open(tar_file_out, mode='w') as tfo:

        try:
            tfo.add(meta_file)
        except tarfile.TarError:
            print('cannot add metafile to tar package')
            raise

        try:
            tfo.add(data_dir)
        except tarfile.TarError:
            print('cannot add data dir to tar package')
            raise

    yield abspath(tar_file_out)

    remove(tar_file_out)


def test_bad_job_id():
    """Test a bad job ID."""
    req = requests.get('http://127.0.0.1:8066/get_state?job_id=12345')
    assert req.status_code == 404


def test_good_upload():
    """Test the good upload."""
    try_good_upload('good', 'OK', 'ingest metadata', 100)


def test_bad_project_upload():
    """Test if the metadata is down."""
    try_good_upload('bad-project', 'FAILED', 'Policy Validation', 0)


def test_bad_hashsum_upload():
    """Test if the metadata is down."""
    try_good_upload('bad-hashsum', 'FAILED', 'ingest files', 0)


def test_bad_metadata_upload():
    """Test if the metadata is down."""
    try_good_upload('bad-mimetype', 'FAILED', 'ingest metadata', 0)


def test_bad_json_upload():
    """Test if the metadata is down."""
    # make_data('bad-json', 'bad-json-md.notjson')
    with test_data('bad-json', 'bad-json-md.notjson') as fpath:
        try_good_upload1(fpath, 'FAILED', 'load metadata', 0)


def test_bad_tarfile_upload():
    """Test if the metadata is down."""
    try_good_upload('bad-tarfile', 'FAILED', 'open tar', 0)
