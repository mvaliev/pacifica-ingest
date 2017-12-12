#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Primary celery process."""
from __future__ import absolute_import
from celery import Celery
from . import settings


INGEST_APP = Celery('ingest_backend', include=['ingest.backend.tasks'])

INGEST_APP.config_from_object(settings)

# Optional configuration, see the application user guide.
INGEST_APP.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)
