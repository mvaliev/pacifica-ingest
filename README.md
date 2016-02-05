# pacifica-ingest
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
```

# API Examples

All calls to the data ingest service are based on a unique ID.

```
MY_INGEST_UUID=`uuidgen`
```


