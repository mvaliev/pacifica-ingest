#!/usr/bin/python
"""Utilities and classes for unbundling and archiving a tar file."""
from __future__ import print_function
import tarfile
import json
import hashlib
import time
import requests
import os

from utils import get_unique_id


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
        """Read wrapper for requests that calculates the hashcode inline."""
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
            url = self.server + str(self.file_id)

            headers = {}
            headers['Last-Modified'] =  mod_time
            headers['Content-Type'] =  'application/octet-stream'
            headers['Content-Length'] =  size_str

            req = requests.put(
                url,
                data=self,
                headers=headers
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
    files = {}
    start_id = -999
    transaction_id = -999
    file_count = -999

    meta_blob = None

    def __init__(self):
        """Constructor."""
        pass

    def load_meta(self, tar):
        """Load the metadata from a tar file into searchable structures."""
        string = tar.extractfile('metadata.txt').read()

        meta_list = json.loads(string)

        # get the start index for the file
        self.file_count = file_count(tar)
        self.transaction_id = get_unique_id(1, 'transaction')
        self.start_id = get_unique_id(self.file_count, 'file')

        self.files = {}

        # all we care about for now is the hash and the file path
        id = self.start_id
        for meta in meta_list:
            if meta['destinationTable'] == 'Files':
                meta['_id'] = id
                #file_element = {}
                #file_element['id'] = str(id)
                #file_element['meta'] = meta

                self.files[str(id)] = meta

                #self.files.append(file_element)
                id+=1

        self.meta_blob = meta_list

    def get_hash(self, file_id):
        """Return the hash string for a file name."""
        file_element = self.files[file_id]
        # remove filetype if there is one
        file_hash = file_element['hashsum'].replace('sha1:', '')
        return file_hash

    def get_fname(self, file_id):
        file_element = self.files[file_id]
        name = file_element['name']
        return name

    def get_subdir(self, file_id):
        file_element = self.files[file_id]
        name = file_element['subdir']
        return name


# pylint: disable=too-few-public-methods
class TarIngester(object):
    """Class to read a tar file and upload it to the metadata and file archives."""

    tar = None
    meta = None

    def __init__(self, tar, meta):
        """Constructor for TarIngester class."""
        self.tar = tar
        self.meta = meta

    def ingest(self):
        """Ingest a tar file into the file archive."""

        archivei_server = os.getenv('ARCHIVEINTERFACE_SERVER', '127.0.0.1')
        archivei_port = os.getenv('ARCHIVEINTERFACE_PORT', '8080')
        archivei_url = 'http://{0}:{1}/'.format(archivei_server, archivei_port)

        for file_id, element in self.meta.files.items():
            #file_id = element['id']
            file_hash = self.meta.get_hash(file_id)
            name = self.meta.get_fname(file_id)

            path = self.meta.get_subdir(file_id) + '/' + self.meta.get_fname(file_id)

            info = self.tar.getmember(path)
            print(info.name)
            ingest = FileIngester(file_hash, archivei_url, file_id)
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
