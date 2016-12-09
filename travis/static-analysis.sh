#!/bin/bash
pylint --rcfile=pylintrc IngestServer.py settings.py ingest
radon cc *.py ingest
