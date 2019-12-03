#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test ingest with a disabled archive interface."""
from __future__ import print_function, absolute_import
from common_methods_test import try_good_upload1, try_good_move
from upload_test import data_load


# this is a long name but descriptive.
# pylint: disable=invalid-name
def test_bad_archiveinterface_upload():
    """Test if the archive interface is down."""
    with data_load('good') as fpath:
        try_good_upload1(fpath, 'FAILED', 'ingest files', 0, 10)
    # try_good_upload('good', 'FAILED', 'ingest files', 0, 10)
# pylint: enable=invalid-name


def test_bad_ai_move():
    """Test the good move."""
    try_good_move('move-md', 'FAILED', 'move files', 0, 10)
