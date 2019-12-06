#!/usr/bin/python
# -*- coding: utf-8 -*-
""" pytest fixture definition. """
from os.path import join, dirname, abspath
from os import listdir, mkdir
from shutil import copy, rmtree
import pytest

_THIS_DIR = dirname(abspath(__file__))
_DATA_DIR = join(_THIS_DIR, 'test_data')


@pytest.fixture(scope='session', autouse=True)
def my_data():
    """test."""
    # tmpdir = tmpdir_factory.getbasetemp()
    tmpdir = join(_DATA_DIR, 'tmp')
    mkdir(tmpdir)

    print('Starting test in Data dir=', tmpdir)

    files_to_copy = ['bad-hashsum.tar',	'bad-mimetype.tar',	'bad-tarfile.tar',
                     'bad-json.tar', 'bad-project.tar', 'good.tar']

    for fname in files_to_copy:
        copy(join(_DATA_DIR, fname), join(tmpdir, fname))

    print('dir listing', listdir(tmpdir))
    yield tmpdir
    rmtree(tmpdir)
    print('Finished test in Data dir=', _DATA_DIR)
