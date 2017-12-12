#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Global static variables."""
from os import getenv

CHERRYPY_CONFIG = getenv('CHERRYPY_CONFIG', 'server.conf')
