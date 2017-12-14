#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ingest Server Main."""
import cherrypy
from ingest.__main__ import error_page_default, main
from ingest.rest import Root
from ingest.globals import CHERRYPY_CONFIG


cherrypy.config.update({'error_page.default': error_page_default})
# pylint doesn't realize that application is actually a callable
# pylint: disable=invalid-name
application = cherrypy.Application(Root(), '/', CHERRYPY_CONFIG)
# pylint: enable=invalid-name

if __name__ == '__main__':
    main()
