#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test ingest with good uploads of good and bad data."""
from __future__ import print_function, absolute_import
from contextlib import contextmanager
import tarfile
from os.path import join, dirname, abspath
from os import remove, chdir, getcwd
from shutil import copy, Error
import requests
from common_methods_test import try_good_upload, try_good_upload1

_THIS_DIR = dirname(abspath(__file__))
_DATA_DIR = join(_THIS_DIR, 'test_data')
_META_DATA_DIR = join(_DATA_DIR, 'metadata-files')


@contextmanager
def data_load(prefix, custom_meta_file=None):
    """generate data for tests."""
    if custom_meta_file:
        meta_file_in = join(_META_DATA_DIR, custom_meta_file)
    else:
        meta_file_in = join(_META_DATA_DIR, '%s-md.json' % prefix)
    data_dir = join(_DATA_DIR, 'data')

    old_dir = getcwd()
    work_dir = _DATA_DIR
    chdir(work_dir)
    meta_file = 'metadata.txt'
    bundle = '%s.tar' % prefix
    data_dir = 'data'

    try:
        copy(meta_file_in, meta_file)
    except Error:
        print('problems copying metafile')
        raise

    with tarfile.open(bundle, mode='w') as tfo:

        try:
            tfo.add(meta_file)
            tfo.add(data_dir)
        except tarfile.TarError:
            print('cannot create tar package')
            raise

    yield abspath(bundle)

    chdir(work_dir)
    remove(bundle)
    remove(meta_file)
    chdir(old_dir)

#
# def test_bad_job_id():
#     """Test a bad job ID."""
#     req = requests.get('http://127.0.0.1:8066/get_state?job_id=12345')
#     assert req.status_code == 404


def test_good_upload():
    """Test the good upload."""
    # try_good_upload('good', 'OK', 'ingest metadata', 100)
    with data_load('good') as fpath:
        try_good_upload1(fpath, 'OK', 'ingest metadata', 100)


def test_bad_project_upload():
    """Test if the metadata is down."""
    # try_good_upload('bad-project', 'FAILED', 'Policy Validation', 0)
    with data_load('bad-project') as fpath:
        try_good_upload1(fpath, 'FAILED', 'Policy Validation', 0)


def test_bad_hashsum_upload():
    """Test if the metadata is down."""
    # try_good_upload('bad-hashsum', 'FAILED', 'ingest files', 0)
    with data_load('bad-hashsum') as fpath:
        try_good_upload1(fpath, 'FAILED', 'FAILED', 'ingest files', 0)

# def test_bad_metadata_upload():
#     """Test if the metadata is down."""
#     try_good_upload('bad-mimetype', 'FAILED', 'ingest metadata', 0)
#
#
# def test_bad_json_upload():
#     """Test if the metadata is down."""
#     # make_data('bad-json', 'bad-json-md.notjson')
#     with data_load('bad-json', 'bad-json-md.notjson') as fpath:
#         try_good_upload1(fpath, 'FAILED', 'load metadata', 0)
#
#
# def test_bad_tarfile_upload():
#     """Test if the metadata is down."""
#     try_good_upload('bad-tarfile', 'FAILED', 'open tar', 0)
