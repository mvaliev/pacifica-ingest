#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Index server unit and integration tests."""
import os
import unittest
from tempfile import mkstemp
from ingest.__main__ import cmd
from ingest.orm import IngestState, BaseModel, read_state
from playhouse.test_utils import test_database
from peewee import SqliteDatabase


class TestEntryPoints(unittest.TestCase):
    """Test the entry points for console and gui."""

    def test_job_subcommand(self):
        """Test the job subcommand for updating job state."""
        rwfd, fname = mkstemp()
        os.close(rwfd)
        with test_database(SqliteDatabase(fname), (BaseModel, IngestState)):
            IngestState.create(
                job_id=999,
                state='ERROR',
                task='unbundling',
                task_percent=42.3
            )
            IngestState.database_close()
            cmd([
                'job',
                '--task=unbundling',
                '--job-id=999',
                '--state=OK',
                '--task-percent=100.0',
                '--exception=Badness'
            ])
            record = read_state(999)
            self.assertEqual(record.state, 'OK')
            self.assertEqual(record.task_percent, 100.0)
