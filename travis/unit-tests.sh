#!/bin/bash
coverage run --include='ingest*' -p -m celery -A ingest.backend worker --loglevel=info &
CELERY_PID=$!
coverage run --include='ingest*' -p IngestServer.py &
SERVER_PID=$!
coverage run --include='ingest*' -m pytest -v
celery control shutdown || true
kill $SERVER_PID $CELERY_PID
wait
sleep 10
kill -9 $SERVER_PID $CELERY_PID || true
wait
coverage combine -a .coverage*
coverage report --show-missing
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
