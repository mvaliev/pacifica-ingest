#!/bin/bash -xe

pylint --extension-pkg-whitelist=pycurl ./
pylint --extension-pkg-whitelist=pycurl ingest_backend
