#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test ingest."""
import os
import mock
import peewee
import requests
from pacifica.ingest.orm import OrmSync, IngestState


@mock.patch.object(IngestState, 'database_connect')
def test_bad_db_connection(mock_is_table_exists):
    """Test a failed db connection."""
    mock_is_table_exists.side_effect = peewee.OperationalError(
        mock.Mock(), 'Error')
    hit_exception = False
    os.environ['DATABASE_CONNECT_ATTEMPTS'] = '1'
    os.environ['DATABASE_CONNECT_WAIT'] = '1'
    try:
        OrmSync.dbconn_blocking()
    except peewee.OperationalError:
        hit_exception = True
    assert hit_exception


def test_rest_root_status():
    """Test the root level status page."""
    resp = requests.get('http://127.0.0.1:8066')
    assert resp.status_code == 200, 'Status code should be 200 OK'
    assert 'message' in resp.json(), 'Status should be object with message key.'
    assert resp.json()['message'] == 'Pacifica Ingest Up and Running', 'message should be specific.'
