#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test ingest with a disabled policy server."""
from __future__ import print_function, absolute_import
from common_methods_test import try_good_upload
from upload_test import data_load


def test_bad_policy_upload():
    """Test if the policy server is down."""
    with data_load('good') as fpath:
        try_good_upload(fpath, 'FAILED', 'Policy Validation', 0, 10)
    # try_good_upload('good', 'FAILED', 'Policy Validation', 0, 10)
