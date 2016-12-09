#!/usr/bin/python
"""Utilities and classes for unbundling and archiving a tar file."""
from __future__ import print_function
import tarfile
import json
import hashlib
import time
import requests


class FileIngester(object):
    """Class to ingest a single file from a tar file into the file archives."""

    fileobj = None
    file_id = 0
    recorded_hash = ''
    hashval = None
    server = ''

    def __init__(self, hashcode, server, file_id):
        """Constructor for FileIngester class."""
        self.hashval = hashlib.sha1()
        self.recorded_hash = hashcode
        self.server = server
        self.file_id = file_id

    def read(self, size):
        """Read wrapper for pycurl that calculates the hashcode inline."""
        buf = self.fileobj.read(size)
        # running checksum
        self.hashval.update(buf)
        return buf

    def validate_hash(self):
        """Validate that the calculated hash matches the hash uploaded in the tar file."""
        file_hash = self.hashval.hexdigest()
        if self.recorded_hash == file_hash:
            return True
        return False

    def upload_file_in_file(self, info, tar):
        """Upload a file from inside a tar file."""
        try:
            self.fileobj = tar.extractfile(info)
            size = self.fileobj.size
            size_str = str(size)
            mod_time = time.ctime(info.mtime)
            self.fileobj.seek(0)
            req = requests.put(
                self.server + str(self.file_id),
                data=self,
                headers=(
                    ('Last-Modified', mod_time),
                    ('Content-Type', 'application/octet-stream'),
                    ('Content-Length', size_str)
                )
            )
            self.fileobj.close()
            body = req.text
            try:
                ret_dict = json.loads(body)
                msg = ret_dict['message']
                print(msg)
                size = int(ret_dict['total_bytes'])
                if size != info.size:
                    return False
            # pylint: disable=broad-except
            except Exception as ex:
                print(ex)
                return False
            # pylint: enable=broad-except

            success = self.validate_hash()
            print('validated = ' + str(success))
            if not success:
                # roll back upload
                return False
            return success
        # pylint: disable=broad-except
        except Exception as ex:
            print(ex)
        # pylint: enable=broad-except


class MetaParser(object):
    """Class used to hold and search metadata."""

    # entire metadata
    meta = None
    # a map of filenames to hashcodes
    files = []
    start_id = -999
    transaction_id = -999

    def __init__(self, transaction_id, start_id):
        """Constructor."""
        self.transaction_id = transaction_id
        self.start_id = start_id

    @staticmethod
    def load_meta(tar):
        """Load the metadata from a tar file into searchable structures."""
        string = tar.extractfile('metadata.txt').read()
        received = json.loads(string)
        return received

    def get_hash(self, file_id):
        """Return the hash string for a file name."""
        file_element = self.files[file_id]
        # remove filetype
        file_hash = file_element['hash'].replace('sha1:', '')
        return file_hash

    def get_fname(self, file_id):
        """Return the hash string for a file name."""
        file_element = self.files[file_id]
        # remove filetype
        file_hash = file_element['name']
        return file_hash


# pylint: disable=too-few-public-methods
class TarIngester(object):
    """Class to read a tar file and upload it to the metadata and file archives."""

    tar = None
    meta = None
    server = ''
    start_id = -999
    transaction_id = -999

    def __init__(self, tar, meta, server):
        """Constructor for TarIngester class."""
        self.tar = tar
        self.meta = meta
        self.server = server

    def ingest(self):
        """Ingest a tar file into the metadata and file archives."""
        keys = self.meta.files.keys()
        for file_id in keys:
            file_hash = self.meta.get_hash(file_id)
            name = self.meta.get_fname(file_id)
            info = self.tar.getmember(name)
            print(info.name)
            ingest = FileIngester(file_hash, self.server, file_id)
            ingest.upload_file_in_file(info, self.tar)
        return True
# pylint: enable=too-few-public-methods


def get_clipped(fname):
    """Return a file path with the data separator removed."""
    return fname.replace('data/', '')


def open_tar(fpath):
    """Seek to the location of fpath, returns a file stream pointer and file size."""
    # check validity
    if not tarfile.is_tarfile(fpath):
        return None

    # open tar file
    try:
        tar = tarfile.open(fpath, 'r:')
    except tarfile.TarError:
        print('Error opening: ' + fpath)
        return None

    return tar


def file_count(tar):
    """
    Retrieve the file count for a tar file.

    Does not count metadata.txt as that is not uploaded to the file archive
    """
    members = tar.getmembers()
    # don't count the metadata.txt file
    return len(members) - 1
