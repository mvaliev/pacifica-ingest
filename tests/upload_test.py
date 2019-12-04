#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test ingest with good uploads of good and bad data."""
from __future__ import print_function, absolute_import
import contextlib
import tarfile
from os.path import join, dirname, abspath
from os import remove, chdir, getcwd
from shutil import copy
import requests
from common_methods_test import try_good_upload


_THIS_DIR = dirname(abspath(__file__))
_DATA_DIR = join(_THIS_DIR, 'test_data')
_META_DATA_DIR = join(_DATA_DIR, 'metadata-files')


@contextlib.contextmanager
def data_load(prefix, custom_meta_file=None):
    """
    Generate data for tests.

    It assumed that data folder is located in tests/test_data
    and that metadata files are located in tests/test_data/metadata-files.

    Parameters:
        prefix (str): metadata file prefix (*-md.json)
        custom_meta_file (str): custom name for metadata file
    """
    if custom_meta_file:
        meta_file_in = join(_META_DATA_DIR, custom_meta_file)
    else:
        meta_file_in = join(_META_DATA_DIR, '%s-md.json' % prefix)

    old_dir = getcwd()
    work_dir = _DATA_DIR
    chdir(work_dir)
    meta_file = 'metadata.txt'
    bundle = '%s.tar' % prefix
    data_dir = 'data'

    try:
        copy(meta_file_in, meta_file)
    except OSError:
        print('\n problems copying metafile \n%s' % meta_file_in)
        raise

    with tarfile.open(bundle, mode='w') as tfo:
        try:
            tfo.add(meta_file)
            tfo.add(data_dir)
        except tarfile.TarError:
            print('cannot create tar package')
            raise

    try:
        yield join(work_dir, bundle)
    finally:
        chdir(work_dir)
        remove(bundle)
        remove(meta_file)
        chdir(old_dir)


def data_up(prefix, custom_meta_file=None):
    """
    Generate data for tests.

    It assumed that data folder is located in tests/test_data
    and that metadata files are located in tests/test_data/metadata-files.

    Parameters:
        prefix (str): metadata file prefix (*-md.json)
        custom_meta_file (str): custom name for metadata file
    """
    if custom_meta_file:
        meta_file_in = join(_META_DATA_DIR, custom_meta_file)
    else:
        meta_file_in = join(_META_DATA_DIR, '%s-md.json' % prefix)

    old_dir = getcwd()
    work_dir = _DATA_DIR
    chdir(work_dir)
    meta_file = 'metadata.txt'
    # bundle = '%s.tar' % prefix
    bundle = 'test.tar'
    data_dir = 'data'

    try:
        copy(meta_file_in, meta_file)
    except OSError:
        print('\n problems copying metafile \n%s' % meta_file_in)
        raise

    with tarfile.open(bundle, mode='w') as tfo:
        try:
            tfo.add(meta_file)
            tfo.add(data_dir)
        except tarfile.TarError:
            print('cannot create tar package')
            raise

    chdir(old_dir)

    return join(work_dir, bundle)


def data_up1(prefix, custom_meta_file=None):
    """
    Generate data for tests.

    It assumed that data folder is located in tests/test_data
    and that metadata files are located in tests/test_data/metadata-files.

    Parameters:
        prefix (str): metadata file prefix (*-md.json)
        custom_meta_file (str): custom name for metadata file
    """
    if custom_meta_file:
        meta_file_in = join(_META_DATA_DIR, custom_meta_file)
    else:
        meta_file_in = join(_META_DATA_DIR, '%s-md.json' % prefix)

    old_dir = getcwd()
    work_dir = _DATA_DIR
    chdir(work_dir)
    meta_file = 'metadata.txt'
    bundle = '%s.tar' % prefix
    data_dir = 'data'

    try:
        copy(meta_file_in, meta_file)
    except OSError:
        print('\n problems copying metafile \n%s' % meta_file_in)
        raise

    with tarfile.open(bundle, mode='w') as tfo:
        try:
            tfo.add(meta_file)
            tfo.add(data_dir)
        except tarfile.TarError:
            print('cannot create tar package')
            raise

    chdir(old_dir)

    return join(work_dir, bundle)



def test_bad_job_id():
    """Test a bad job ID."""
    req = requests.get('http://127.0.0.1:8066/get_state?job_id=12345')
    assert req.status_code == 404


def test_good_upload():
    """Test the good upload."""
    with data_load('good') as fpath:
        try_good_upload(fpath, 'OK', 'ingest metadata', 100)


def test_bad_project_upload():
    """Test if the metadata is down."""
    with data_load('bad-project') as fpath:
        try_good_upload(fpath, 'FAILED', 'Policy Validation', 0)


def test_bad_hashsum_upload():
    """Test if the metadata is down."""
    with data_load('bad-hashsum') as fpath:
        try_good_upload(fpath, 'FAILED', 'ingest files', 0)


def test_bad_metadata_upload():
    """Test if the metadata is down."""
    with data_load('bad-mimetype') as fpath:
        try_good_upload(fpath, 'FAILED', 'ingest metadata', 0)


def test_bad_json_upload():
    """Test if the metadata is down."""
    with data_load('bad-json', 'bad-json-md.notjson') as fpath:
        try_good_upload(fpath, 'FAILED', 'load metadata', 0)


def test_bad_tarfile_upload():
    """Test if the metadata is down."""
    fpath = join(_DATA_DIR, 'bad-tarfile.tar')
    try_good_upload(fpath, 'FAILED', 'open tar', 0)
