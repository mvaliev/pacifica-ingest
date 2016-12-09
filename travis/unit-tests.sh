#!/bin/bash
coverage run --include='ingest*' -p -m celery -A ingest.backend worker --loglevel=info &
CELERY_PID=$!
coverage run --include='ingest*' -p IngestServer.py &
SERVER_PID=$!
coverage run --include='ingest*' -m pytest -v
celery control shutdown || true
kill -9 $SERVER_PID
wait
coverage combine -a .coverage*
coverage report --show-missing
codeclimate-test-reporter
