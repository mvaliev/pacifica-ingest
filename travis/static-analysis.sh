#!/bin/bash
pylint --rcfile=pylintrc IngestServer.py DatabaseCreate.py settings.py ingest
radon cc *.py ingest
