#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test ingest with good uploads of good and bad data."""
from __future__ import print_function, absolute_import

import tarfile
from os.path import join, dirname, abspath
from shutil import copy, Error

_THIS_DIR = dirname(abspath(__file__))
_DATA_DIR = join(_THIS_DIR, 'test_data')
_META_DATA_DIR = join(_DATA_DIR, "metadata-files")


def get_data_dir():
    """return common data directory."""
    return _DATA_DIR


def make_data(prefix, custom_meta_file=None):
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

        return abspath(tar_file_out)


if __name__ == "__main__":
    print(make_data('good'))
