#!/bin/bash
coverage run --include='ingest*' -p -m celery -A ingest.backend worker --loglevel=info -c 1 -P solo &
CELERY_PID=$!
coverage run --include='ingest*' -p IngestServer.py &
SERVER_PID=$!
coverage run --include='ingest*' -m -p pytest -v
python -m celery control shutdown || true
kill $SERVER_PID $CELERY_PID
wait
sleep 3
kill -9 $SERVER_PID $CELERY_PID || true
wait
coverage combine -a .coverage*
coverage report --show-missing --fail-under=100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
