#!/usr/bin/python
"""Test ingest with a disabled archive interface."""
from __future__ import print_function
from ingest.test import try_good_upload


# this is a long name but descriptive.
# pylint: disable=invalid-name
def test_bad_archiveinterface_upload():
    """Test if the archive interface is down."""
    try_good_upload('good', 'FAILED', 'ingest files', 0)
# pylint: enable=invalid-name
