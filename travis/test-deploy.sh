#!/bin/bash
docker build -t pacifica/ingest-backend -f Dockerfile.celery .
docker build -t pacifica/ingest-frontend -f Dockerfile.wsgi .
