#!/bin/bash -xe

pylint --extension-pkg-whitelist=pycurl *.py
pylint --extension-pkg-whitelist=pycurl ingest_backend
