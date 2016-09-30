# pacifica-ingest
[![Build Status](https://travis-ci.org/EMSL-MSC/pacifica-ingest.svg?branch=master)](https://travis-ci.org/EMSL-MSC/pacifica-ingest)
[![Code Climate](https://codeclimate.com/github/EMSL-MSC/pacifica-ingest/badges/gpa.svg)](https://codeclimate.com/github/EMSL-MSC/pacifica-ingest)
[![Test Coverage](https://codeclimate.com/github/EMSL-MSC/pacifica-ingest/badges/coverage.svg)](https://codeclimate.com/github/EMSL-MSC/pacifica-ingest/coverage)
[![Issue Count](https://codeclimate.com/github/EMSL-MSC/pacifica-ingest/badges/issue_count.svg)](https://codeclimate.com/github/EMSL-MSC/pacifica-ingest)

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


