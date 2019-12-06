#!/usr/bin/python
# -*- coding: utf-8 -*-
"""pytest fixture definition."""
from os.path import join, dirname, abspath
from os import listdir, mkdir
from shutil import copy, rmtree
import tarfile
import pytest

_THIS_DIR = dirname(abspath(__file__))
_DATA_DIR = join(_THIS_DIR, 'test_data')
_TMP_DATA_DIR = join(_DATA_DIR, 'tmp1')
_META_DATA_DIR = join(_DATA_DIR, 'metadata-files')


def bundle_up(meta_file, data_dir, bundle_file):
    """
    Generate data for tests.

    It assumed that data folder is located in tests/test_data
    and that metadata files are located in tests/test_data/metadata-files.

    Parameters:
        meta_file(str): path to metadata file
        data_dir (str): path to data directory
        bundle_file (str): path to bundle (tar file)
    """
    with tarfile.open(bundle_file, mode='w') as tfp:
        try:
            tfp.add(meta_file, arcname='metadata.txt')
            tfp.add(data_dir, arcname='data')
        except tarfile.TarError:
            print('cannot create tar package')
            raise

    return bundle_file


@pytest.fixture(scope='session', autouse=True)
def my_data():
    """test."""
    # tmpdir = tmpdir_factory.getbasetemp()
    tmpdir = _TMP_DATA_DIR
    try:
        mkdir(tmpdir)
    except FileExistsError:
        print('Directory exists')
        raise

    print('Starting test in data dir=', tmpdir)

    files_to_copy = ['bad-hashsum.tar', 'bad-tarfile.tar',
                     'bad-move-md.json', 'move-md.json']

    for fname in files_to_copy:
        copy(join(_DATA_DIR, fname), join(tmpdir, fname))

    print('dir listing', listdir(tmpdir))

    file_array = []

    for prefix in ['good', 'bad-project', 'bad-mimetype', 'bad-hashsum']:
        file_array.append(('%s-md.json' % prefix, '%s.tar' % prefix))

    file_array.append(('bad-json-md.notjson', 'bad-json.tar'))

    data_dir = join(_DATA_DIR, 'data')
    for meta_file, bundle_file in file_array:
        meta_file = join(_META_DATA_DIR, meta_file)
        bundle_file = join(_TMP_DATA_DIR, bundle_file)

        try:
            bundle_up(meta_file, data_dir, bundle_file)
        except tarfile.TarError:
            rmtree(tmpdir)
            raise

    yield tmpdir
    rmtree(tmpdir)
    print('Finished test in Data dir=', _DATA_DIR)
