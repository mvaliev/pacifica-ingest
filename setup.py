#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the ingest."""
from pip.req import parse_requirements
from setuptools import setup

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements('requirements.txt', session='hack')

setup(name='PacificaIngest',
      version='1.0',
      description='Pacifica Ingest',
      author='David Brown',
      author_email='david.brown@pnnl.gov',
      packages=['ingest', 'ingest.backend', 'ingest.test'],
      scripts=['IngestServer.py', 'DatabaseCreate.py'],
      entry_points={
          'console_scripts': [
              'IngestCMD=ingest.__main__:cmd',
              'IngestServer=ingest.__main__:main'
          ]
      },
      install_requires=[str(ir.req) for ir in INSTALL_REQS])
