"""
    testable utilities for ingest
"""

from urlparse import parse_qs
import json

import pycurl
from StringIO import StringIO

import os

from time import sleep

# pylint: disable=bare-except
# pylint: disable=broad-except

def get_job_id(environ):
    """
    parse the parameters for a request from the environ dictionary
    """
    try:
        args = parse_qs(environ['QUERY_STRING'])

        if args:
            job_id = long(args.get('job_id', [''])[0])
            return job_id

        return (None, None)

    except:
        return (None, None)

def valid_request(environ):
    """
    catch and handle bogus requests (ex. faveicon)
    """
    info = environ['PATH_INFO']
    return info == '/get_state'


def create_invalid_return():
    """
    create an error message
    """
    status = '404 NOT FOUND'

    response_body = ''

    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    return (status, response_headers, response_body)

def create_return_params(response_body):
    """
    creates return parameters
    """

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    return (status, response_headers, response_body)

def create_state_return(record):
    """
    creates the dictionary containing the start and stop index
    packs the message components
    """
    state = {'job_id' : record.job_id, 'state' : record.state, 'task': record.task,\
             'task_percent': str(record.task_percent)}
    response_body = json.dumps(state)

    return create_return_params(response_body)


def get_unique_id():
    """
    returns a unique job id from the id server
    """

    buf = StringIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, 'http://127.0.0.1:8051/getid?range=1&mode=upload_job')
    curl.setopt(curl.WRITEDATA, buf)
    curl.perform()
    curl.close()

    body = buf.getvalue()

    info = json.loads(body)

    job_id = info['startIndex']

    return job_id


def upload_file(filepath, uid):
    """
    returns a unique job id from the id server
    """

    try:
        size = os.path.getsize(filepath)
        sizeStr = str(size)

        buf = StringIO()

        curl = pycurl.Curl()

        curl.setopt(pycurl.PUT, True)

        curl.setopt(pycurl.HTTPHEADER,['Last-Modified: Sun, 06 Nov 1994 08:49:37 GMT',
                                       'Content-Type: application/octet-stream',
                                       'Content-Length: ' + sizeStr
                                       ])

        fin = open(filepath,'rb')
        #global fo
        #fo = fin
        curl.setopt(curl.READFUNCTION, fin.read)
        curl.setopt(curl.INFILESIZE, size)
        curl.setopt(curl.URL, 'http://130.20.227.120:8067/' + str(uid))
        curl.setopt(curl.WRITEDATA, buf)
        curl.perform()
        curl.close()

        body = buf.getvalue()
        print body
        return body
    except Exception, ex:
        print ex


def rename_bundle(environ, job_id):
    """
    receive the tar file and save it locally
    """
    try:

        if environ['REQUEST_METHOD'] == 'POST':

            # ctype, pdict = cgi.parse_header(environ['CONTENT_TYPE'])

            path = environ['HTTP_X_FILE']

            root = os.path.dirname(path)

            name = str(job_id) + ".tar"
            name = os.path.join(root, name)

            os.rename(path, name)

            return name


    except Exception, ex:
        print ex.message


def receive(environ, job_id):
    """
    receive the tar file and save it locally
    """
    try:
        if environ['REQUEST_METHOD'] == 'POST':
            root = 'c:\\temp'
            name = str(job_id) + ".tar"
            name = os.path.join(root, name)
            file_out = open(name, 'wb')

            block_size = 1024 * 1024
            content_length = int(environ['CONTENT_LENGTH'])

            print "content length " + str(content_length)

            while content_length > 0:
                if content_length > block_size:
                    buf = environ['wsgi.input'].read(block_size)
                else:
                    buf = environ['wsgi.input'].read(content_length)

                file_out.write(buf)
                content_length -= len(buf)

            file_out.close()

            return name

    except Exception, ex:
        print ex.message
        return ""




