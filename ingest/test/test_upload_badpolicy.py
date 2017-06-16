#!/usr/bin/python
"""Test ingest with a disabled policy server."""
from __future__ import print_function
from ingest.test import try_good_upload


def test_bad_policy_upload():
    """Test if the policy server is down."""
    try_good_upload('good', 'FAILED', 'Policy Validation', 0)
