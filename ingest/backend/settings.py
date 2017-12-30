#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Celery Setting."""
from os import getenv

# pylint: disable=too-few-public-methods


class CeleryConfig(object):
    """Celery configuration object."""

    broker_url = getenv(
        'BROKER_URL',
        '{transport}://{user}:{password}@{server}:{port}/{vhost}'.format(
            transport=getenv('BROKER_TRANSPORT', 'amqp'),
            user=getenv('BROKER_USER', 'guest'),
            password=getenv('BROKER_PASS', 'guest'),
            server=getenv('BROKER_SERVER', '127.0.0.1'),
            port=getenv('BROKER_PORT', 5672),
            vhost=getenv('BROKER_VHOST', '/')
        )
    )
    result_backend = getenv('BACKEND_URL', 'rpc://')
# pylint: enable=too-few-public-methods
