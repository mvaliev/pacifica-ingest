#!/usr/bin/python
"""Testable utilities for ingest."""
from __future__ import print_function
import os
from urlparse import parse_qs
import json
import requests

# pylint: disable=bare-except
# pylint: disable=broad-except


def get_job_id(environ):
    """Parse the parameters for a request from the environ dictionary."""
    try:
        args = parse_qs(environ['QUERY_STRING'])
        if args:
            job_id = int(args.get('job_id', [''])[0])
            return job_id
        return (None, None)
    except:
        return (None, None)


def valid_request(environ):
    """Catch and handle bogus requests (ex. faveicon)."""
    info = environ['PATH_INFO']
    return info == '/get_state'


def create_invalid_return():
    """Create an error message."""
    status = '404 NOT FOUND'
    response_body = 'Invalid'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    return (status, response_headers, response_body)


def create_return_params(response_body):
    """Create return parameters."""
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    return (status, response_headers, response_body)


def create_state_return(record):
    """Create the dictionary containing the start and stop index packs the message components."""
    state = {'job_id': record.job_id, 'state': record.state, 'task': record.task,
             'task_percent': str(record.task_percent)}
    response_body = json.dumps(state)
    return create_return_params(response_body)


def get_unique_id(range, mode):
    """Return a unique job id from the id server."""
    uniqueid_server = os.getenv('UNIQUEID_SERVER', '127.0.0.1')
    uniqueid_port = os.getenv('UNIQUEID_PORT', '8051')
    
    url = 'http://{0}:{1}/getid?range={2}&mode={3}'.format(uniqueid_server, uniqueid_port, range, mode)
    
    req = requests.get(url)
    body = req.text
    info = json.loads(body)
    unique_id = info['startIndex']

    return unique_id


#def upload_file(filepath, uid):
#    """Return a unique job id from the id server."""
#    try:
#        archivei_server = os.getenv('ARCHIVEINTERFACE_SERVER', '127.0.0.1')
#        archivei_port = os.getenv('ARCHIVEINTERFACE_PORT', '8080')
#        archivei_url = 'http://{0}:{1}/'.format(archivei_server, archivei_port)
#        size = os.path.getsize(filepath)
#        file_size = str(size)
#        body = ''
#        with open(filepath, 'rb') as filedesc:
#            req = requests.put(
#                archivei_url + str(uid),
#                data=filedesc,
#                headers=(
#                    ('Last-Modified', 'Sun, 06 Nov 1994 08:49:37 GMT'),
#                    ('Content-Type', 'application/octet-stream'),
#                    ('Content-Length', file_size)
#                )
#            )
#            body = req.text
#        print(body)
#        return body
#    except Exception as ex:
#        print(ex)


def rename_bundle(environ, job_id):
    """Receive the tar file and save it locally."""
    try:
        if environ['REQUEST_METHOD'] == 'POST':
            # ctype, pdict = cgi.parse_header(environ['CONTENT_TYPE'])
            path = environ['HTTP_X_FILE']
            root = os.path.dirname(path)
            name = str(job_id) + '.tar'
            name = os.path.join(root, name)
            os.rename(path, name)
            return name
    except Exception as ex:
        print(ex.message)


def receive(environ, job_id):
    """Receive the tar file and save it locally."""
    try:
        if environ['REQUEST_METHOD'] == 'POST':
            root = os.getenv('VOLUME_PATH', '/tmp')
            name = str(job_id) + '.tar'
            name = os.path.join(root, name)
            file_out = open(name, 'wb')
            block_size = 1024 * 1024
            content_length = int(environ['CONTENT_LENGTH'])
            print('content length ' + str(content_length))
            while content_length > 0:
                if content_length > block_size:
                    buf = environ['wsgi.input'].read(block_size)
                else:
                    buf = environ['wsgi.input'].read(content_length)

                file_out.write(buf)
                content_length -= len(buf)
            file_out.close()
            return name
    except Exception as ex:
        print(ex.message)
        return ''
