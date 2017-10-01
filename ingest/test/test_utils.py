#!/usr/bin/python
"""Test ingest."""
import mock
import peewee
from ingest.orm import create_tables, IngestState


@mock.patch.object(IngestState, 'table_exists')
def test_bad_db_connection(mock_is_table_exists):
    """Test a failed db connection."""
    mock_is_table_exists.side_effect = peewee.OperationalError(mock.Mock(), 'Error')
    hit_exception = False
    try:
        create_tables(18)
    except peewee.OperationalError:
        hit_exception = True
    assert hit_exception
