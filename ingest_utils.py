"""
    testable utilities for ingest
"""

from urlparse import parse_qs
import json

import pycurl
from StringIO import StringIO

import cgi
import os
import sys

# pylint: disable=bare-except

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
    state = {'state' : record.state, 'task': record.task, 'task_percent': str(record.task_percent)}
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

    return (job_id, body)

def receive(environ):
    """
    receive the tar file and save it locally
    """
    try:

        if environ['REQUEST_METHOD'] == 'POST':
            post = cgi.FieldStorage(
                fp=environ['wsgi.input'],
                environ=environ,
                keep_blank_values=True
            )

            fileitem = post["userfile"]
            if fileitem.file:
                root = 'c:\Temp'
                filename = fileitem.filename.decode('utf8').replace('\\','/').split('/')[-1].strip()
                if not filename:
                    raise Exception('No valid filename specified')
                file_path = os.path.join(self.root, filename)
                # Using with makes Python automatically close the file for you
                counter = 0
                with open(file_path, 'wb') as output_file:
                    # In practice, sending these messages doesn't work
                    # environ['wsgi.errors'].write('Receiving upload ...\n') 
                    # environ['wsgi.errors'].flush()
                    # print 'Receiving upload ...\n'
                    while 1:
                        data = fileitem.file.read(1024)
                        # End of file
                        if not data:
                            break
                        output_file.write(data)
                        counter += 1
                        if counter == 100:
                            counter = 0
                            # environ['wsgi.errors'].write('.') 
                            # environ['wsgi.errors'].flush()
                            # print '.',
    except Exception, e:
        print e.message




