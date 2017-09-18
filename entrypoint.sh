#!/bin/bash
python /usr/src/app/DatabaseCreate.py
uwsgi \
  --http-socket 0.0.0.0:8066 \
  --master \
  --die-on-term \
  --wsgi-file /usr/src/app/IngestServer.py "$@"
