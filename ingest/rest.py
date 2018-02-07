#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ingest Server Main."""
import os
import shutil
import json
import peewee
import cherrypy
from ingest.orm import read_state, update_state
from ingest.utils import get_unique_id, create_state_response
from ingest.backend import tasks


# pylint: disable=too-few-public-methods
class RestIngestState(object):
    """The CherryPy ingest state object."""

    exposed = True

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @cherrypy.tools.json_out()
    def GET(job_id):
        """Get the ingest state for the job."""
        try:
            record = read_state(job_id)
        except peewee.DoesNotExist:
            raise cherrypy.HTTPError(
                '404 Not Found', 'job ID {} does not exist.'.format(job_id))
        return create_state_response(record)
    # pylint: enable=invalid-name


class RestMove(object):
    """Ingest the data from the service."""

    exposed = True

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST():
        """Post the uploaded data."""
        job_id = get_unique_id(1, 'upload_job')
        update_state(job_id, 'OK', 'UPLOADING', 0)
        root = os.getenv('VOLUME_PATH', '/tmp')
        name = str(job_id) + '.json'
        name = os.path.join(root, name)
        with open(name, 'wb') as ingest_fd:
            ingest_fd.write(json.dumps(cherrypy.request.json))
        tasks.move.delay(job_id, name)
        return create_state_response(read_state(job_id))
    # pylint: enable=invalid-name


class RestUpload(object):
    """Ingest the data from the service."""

    exposed = True

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @cherrypy.tools.json_out()
    def POST():
        """Post the uploaded data."""
        job_id = get_unique_id(1, 'upload_job')
        update_state(job_id, 'OK', 'UPLOADING', 0)
        root = os.getenv('VOLUME_PATH', '/tmp')
        name = str(job_id) + '.tar'
        name = os.path.join(root, name)
        with open(name, 'wb') as ingest_fd:
            shutil.copyfileobj(cherrypy.request.body, ingest_fd)
        tasks.ingest.delay(job_id, name)
        return create_state_response(read_state(job_id))
    # pylint: enable=invalid-name


class Root(object):
    """The CherryPy root object."""

    exposed = False
    get_state = RestIngestState()
    upload = RestUpload()
    move = RestMove()
# pylint: enable=too-few-public-methods
