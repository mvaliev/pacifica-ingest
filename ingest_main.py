#!/usr/bin/env python
"""
ingest Server
"""
# disable this for classes Index and Meta (within Index)
# pylint: disable=too-few-public-methods

from wsgiref.simple_server import make_server

import os
import json
import logging

from ingest_orm import IngestState, DB, read_state

from ingest_utils import create_invalid_return, create_state_return, get_job_id, \
                            get_unique_id, create_return_params

from ingest_backend import tasks

from time import sleep

def ping_celery():
    """
    check to see if the celery process to bundle and upload is alive, alive!
    """
    ping_process = tasks.ping.delay()

    tries = 0
    while tries < 5:
        state = ping_process.state
        if state is not None:
            print state
            if state == "PING" or state == "SUCCESS":
                return True
        sleep(1)
        tries += 1

    return False

@DB.atomic()
def application(environ, start_response):
    """
    The wsgi callback
    """

    info = environ['PATH_INFO']

    if info and info == '/get_state':

        job_id = get_job_id(environ)
        record = read_state(job_id)

        if record:
            status, response_headers, response_body = create_state_return(record)
            start_response(status, response_headers)
            return [response_body]

    elif info and info == '/upload':
        # get id from id server
        job_id, body = get_unique_id()

        body = json.dumps({'job_id':job_id})

        tasks.thingy.delay()

        ping_celery()

        status, response_headers, response_body = create_return_params(body)
        start_response(status, response_headers)
        return [body]

    else:
        status, response_headers, response_body = create_invalid_return()
        start_response(status, response_headers)
        return [response_body]

    status, response_headers, response_body = create_invalid_return()
    start_response(status, response_headers)
    return [response_body]

def main():
    """
        entry point for main index server
    """
    peewee_logger = logging.getLogger('peewee')
    peewee_logger.setLevel(logging.DEBUG)
    peewee_logger.addHandler(logging.StreamHandler())

    main_logger = logging.getLogger('index_server')
    main_logger.setLevel(logging.DEBUG)
    main_logger.addHandler(logging.StreamHandler())

    main_logger.info("MYSQL_ENV_MYSQL_DATABASE = " +  os.getenv('MYSQL_ENV_MYSQL_DATABASE'))
    main_logger.info("MYSQL_PORT_3306_TCP_ADDR = " +  os.getenv('MYSQL_PORT_3306_TCP_ADDR'))
    main_logger.info("MYSQL_PORT_3306_TCP_PORT = " +  os.getenv('MYSQL_PORT_3306_TCP_PORT'))
    main_logger.info("MYSQL_ENV_MYSQL_USER = " +  os.getenv('MYSQL_ENV_MYSQL_USER'))
    main_logger.info("MYSQL_ENV_MYSQL_PASSWORD = " +  os.getenv('MYSQL_ENV_MYSQL_PASSWORD'))

    if not IngestState.table_exists():
        IngestState.create_table()

    httpd = make_server('0.0.0.0', 8066, application)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
