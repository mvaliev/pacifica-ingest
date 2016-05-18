"""
    utilities for unbundling 
"""

import tarfile
import os
import pycurl
from StringIO import StringIO

import unicodedata

import json
import hashlib
import time

class FileIngester(object):

    fileobj = None
    id = 0
    recorded_hash = ''
    hashval = None
    server = ''

    def __init__(self, hash, server, id):
        self.hashval = hashlib.sha1()
        self.recorded_hash = hash
        self.server = server
        self.id = id

    def reader(self, size):
        buf = self.fileobj.read(size)

        # running checksum
        self.hashval.update(buf)

        return buf

    def validate_hash(self):
        file_hash = self.hashval.hexdigest()

        if self.recorded_hash == file_hash:
            return True
        return False

    def upload_file_in_file(self, info, tar, uid):
        """
        uploads a file from inside a tar file
        """
        try:
            self.fileobj = tar.extractfile(info)

            size = self.fileobj.size
            sizeStr = str(size)

            buf = StringIO()

            curl = pycurl.Curl()

            curl.setopt(curl.PUT, True)

            mod_time = time.ctime(info.mtime)

            curl.setopt(curl.HTTPHEADER,['Last-Modified: ' + mod_time, 
                                         'Content-Type: application/octet-stream',
                                         'Content-Length: ' + sizeStr
                                         ])

            #assume tar file is open
            self.fileobj.seek(0)

            curl.setopt(curl.READFUNCTION, self.reader)
            curl.setopt(curl.INFILESIZE, size)

            curl.setopt(curl.URL, self.server + str(uid))
            curl.setopt(curl.WRITEDATA, buf)

            curl.perform()
            curl.close()

            self.fileobj.close()

            body = buf.getvalue()

            print body

            try:
                ret_dict = json.loads(body)
                msg = ret_dict['message']
                bytes = int(ret_dict['total_bytes'])
                if bytes != info.size:
                    return False
            except Exception, e:
                return False

            success = self.validate_hash()

            print 'validated = ' + str(success)

            if not success:
                # roll back upload
                return False


            return success
        except Exception, ex:
            print ex

class MetaParser(object):

    meta_dict = None
    file_dict = None

    def load_meta(self, tar):

        string = tar.extractfile('metadata.txt').read()

        self.meta_dict = json.loads(string)

        files = self.meta_dict['file']

        self.file_dict = {}

        for elem in files:
            fname = elem['fileName']
            hash = elem['sha1Hash']
            dir = elem['destinationDirectory']

            # force linux format
            path = dir + '/' +  fname

            self.file_dict [path] = hash

    def pack_meta(self):
        """
        pack metadata into a json object to pass to the metadata archive
        """

    def get_hash(self, fname):
        return self.file_dict[fname]

    def get_clipped(self, fname):
        return fname.replace ('data/', '')



class TarIngester():
    """
    """
    fpath = ''
    server = ''
    id_start = 0

    def __init__(self, fpath, server):
        self.fpath = fpath
        self.server = server

    def open_tar(self, fpath):

        """ 
        seeks to the location of fpath, returns a file stream pointer and file size.
        """
        # check validity
        if not tarfile.is_tarfile(fpath):
            false

        # open tar file
        try:
            tar = tarfile.open(fpath, 'r:')
        except tarfile.TarError, e:
            print "Error opening: " + fpath
            return None

        return tar

    def file_count(self):
        tar = self.open_tar(self.fpath)
        members = tar.getmembers()

        # don't count the metadata.txt file
        return len(members) - 1

    def ingest_tar(self):

        # get the file members
        tar = self.open_tar(self.fpath)

        meta = MetaParser()
        meta.load_meta(tar)

        id = self.id_start

         # get the file members
        members = tar.getmembers()

        for info in members:
            print info.name

            if (info.name != 'metadata.txt'):

                ingest = FileIngester(meta.get_hash(info.name), self.server, id)

                ingest.upload_file_in_file(info, tar, id)

                id += 1


        return True