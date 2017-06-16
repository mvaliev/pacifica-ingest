#!/bin/bash
pylint --rcfile=pylintrc IngestServer.py DatabaseCreate.py settings.py ingest setup.py
radon cc *.py ingest
