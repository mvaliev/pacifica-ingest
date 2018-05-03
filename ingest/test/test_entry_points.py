#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Index server unit and integration tests."""
import os
from tempfile import mkstemp
from ingest.__main__ import cmd
from ingest.orm import IngestState, read_state
from ingest.test.ingest_db_setup import IngestDBSetup


class TestEntryPoints(IngestDBSetup):
    """Test the entry points for console and gui."""

    def test_job_subcommand(self):
        """Test the job subcommand for updating job state."""
        rwfd, _fname = mkstemp()
        os.close(rwfd)
        IngestState.create(
            job_id=998,
            state='ERROR',
            task='unbundling',
            task_percent=42.3
        )
        IngestState.database_close()
        cmd([
            'job',
            '--task=unbundling',
            '--job-id=998',
            '--state=OK',
            '--task-percent=100.0',
            '--exception=Badness'
        ])
        record = read_state(998)
        self.assertEqual(record.state, 'OK')
        self.assertEqual(record.task_percent, 100.0)
