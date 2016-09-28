#!/bin/bash -x

pylint --extension-pkg-whitelist=pycurl *.py
pylint --extension-pkg-whitelist=pycurl ingest_backend
exit 0
