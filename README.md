# Pacifica Ingest
[![Build Status](https://travis-ci.org/pacifica/pacifica-ingest.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-ingest)
[![Build status](https://ci.appveyor.com/api/projects/status/dhniln12ili29kgm?svg=true)](https://ci.appveyor.com/project/dmlb2000/pacifica-ingest)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-ingest/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-ingest)
[![Test Coverage](https://codeclimate.com/github/pacifica/pacifica-ingest/badges/coverage.svg)](https://codeclimate.com/github/pacifica/pacifica-ingest/coverage)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-ingest/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-ingest)

## Docker Badges
[![Frontend Stars](https://img.shields.io/docker/stars/pacifica/ingest-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-frontend/general)
[![Backend Stars](https://img.shields.io/docker/stars/pacifica/ingest-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-backend/general)
[![Frontend Pulls](https://img.shields.io/docker/pulls/pacifica/ingest-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-frontend/general)
[![Backend Pulls](https://img.shields.io/docker/pulls/pacifica/ingest-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-backend/general)
[![Frontend Automated build](https://img.shields.io/docker/automated/pacifica/ingest-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-frontend/builds)
[![Backend Automated build](https://img.shields.io/docker/automated/pacifica/ingest-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-backend/builds)

Pacifica data ingest service to process and validate incoming data from the uploader.

Ingest and validate data from the pacifica-uploader

# Building and Installing

This code depends on the following libraries and python modules:

Docker/docker-compose
Peewee
Celery
MySQL-Python
This is a standard python distutils build process.

```
python ./setup.py build
python ./setup.py install
```

# Running It

To bring up a test instance use docker-compose

```
docker-compose up

test
```

# API Examples

All calls to the data ingest service are based on a unique ID.

```
MY_INGEST_UUID=`uuidgen`
```
