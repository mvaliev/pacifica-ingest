#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Ingest module."""
import os
from sys import argv as sys_argv
from time import sleep
from threading import Thread
from argparse import ArgumentParser, SUPPRESS
import cherrypy
from peewee import OperationalError
from .rest import Root, error_page_default
from .orm import OrmSync, update_state, IngestStateSystem, SCHEMA_MAJOR, SCHEMA_MINOR
from .globals import CONFIG_FILE, CHERRYPY_CONFIG


def stop_later(doit=False):
    """Used for unit testing stop after 60 seconds."""
    if not doit:  # pragma: no cover
        return

    def sleep_then_exit():
        """
        Sleep for 90 seconds then call cherrypy exit.

        Hopefully this is long enough for the end-to-end tests to finish
        """
        sleep(120)
        cherrypy.engine.exit()
    sleep_thread = Thread(target=sleep_then_exit)
    sleep_thread.daemon = True
    sleep_thread.start()


def main(argv=None):
    """Main method to start the httpd server."""
    parser = ArgumentParser(description='Run the cart server.')
    parser.add_argument('--cp-config', metavar='CPCONFIG', type=str,
                        default=CHERRYPY_CONFIG, dest='cpconfig',
                        help='cherrypy config file')
    parser.add_argument('-c', '--config', metavar='CONFIG', type=str,
                        default=CONFIG_FILE, dest='config',
                        help='ingest config file')
    parser.add_argument('-p', '--port', metavar='PORT', type=int,
                        default=8066, dest='port',
                        help='port to listen on')
    parser.add_argument('-a', '--address', metavar='ADDRESS',
                        default='localhost', dest='address',
                        help='address to listen on')
    parser.add_argument('--stop-after-a-moment', help=SUPPRESS,
                        default=False, dest='stop_later',
                        action='store_true')
    args = parser.parse_args(argv)
    OrmSync.dbconn_blocking()
    if not IngestStateSystem.is_safe():
        raise OperationalError('Database version too old {} update to {}'.format(
            '{}.{}'.format(*(IngestStateSystem.get_version())),
            '{}.{}'.format(SCHEMA_MAJOR, SCHEMA_MINOR)
        ))
    stop_later(args.stop_later)
    cherrypy.config.update({'error_page.default': error_page_default})
    cherrypy.config.update({
        'server.socket_host': args.address,
        'server.socket_port': args.port
    })
    cherrypy.quickstart(Root(), '/', args.cpconfig)


def cmd(argv=None):
    """Command line admin tool for managing ingest."""
    parser = ArgumentParser(description='Admin command line tool.')
    parser.add_argument(
        '-c', '--config', metavar='CONFIG', type=str, default=CONFIG_FILE,
        dest='config', help='ingest config file'
    )
    subparsers = parser.add_subparsers(help='sub-command help')
    job_parser = subparsers.add_parser(
        'job', help='job help', description='manage jobs')
    for attr in ['job_id', 'state', 'task', 'task_percent', 'exception']:
        job_parser.add_argument(
            '--{}'.format(attr.replace('_', '-')),
            dest=attr,
            help='set the {}'.format(attr)
        )
    job_parser.set_defaults(func=update_wrapper)
    db_parser = subparsers.add_parser(
        'dbsync',
        description='Update or Create the Database.'
    )
    db_parser.set_defaults(func=dbsync)
    dbchk_parser = subparsers.add_parser(
        'dbchk',
        description='Check database against current version.'
    )
    dbchk_parser.add_argument(
        '--equal', default=False,
        dest='check_equal', action='store_true'
    )
    dbchk_parser.set_defaults(func=dbchk)
    args = parser.parse_args(argv)
    return args.func(args)


def update_wrapper(args):
    """Call update state with appropriate args."""
    return update_state(
        args.job_id,
        args.state,
        args.task,
        args.task_percent,
        args.exception
    )


def bool2cmdint(command_bool):
    """Convert a boolean to either 0 for true  or -1 for false."""
    if command_bool:
        return 0
    return -1


def dbsync(args):
    """Create/Update the database schema to current code."""
    os.environ['INGEST_CONFIG'] = args.config
    OrmSync.dbconn_blocking()
    return OrmSync.update_tables()


def dbchk(args):
    """Check to see if the database is safe to use."""
    os.environ['INGEST_CONFIG'] = args.config
    OrmSync.dbconn_blocking()
    if args.check_equal:
        return bool2cmdint(IngestStateSystem.is_equal())
    return bool2cmdint(IngestStateSystem.is_safe())


if __name__ == '__main__':
    main(sys_argv[1:])
