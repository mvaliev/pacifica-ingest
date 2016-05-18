"""
    utilities and classes for unbundling and archiving a tar file
"""

import tarfile
import pycurl
from StringIO import StringIO

import json
import hashlib
import time

class FileIngester(object):
    """
    class to ingest a single file from a tar file into the file archives
    """

    fileobj = None
    id = 0
    recorded_hash = ''
    hashval = None
    server = ''

    def __init__(self, hash, server, id):
        """
        constructor for FileIngester class
        """

        self.hashval = hashlib.sha1()
        self.recorded_hash = hash
        self.server = server
        self.id = id

    def reader(self, size):
        """
        read wrapper for pycurl that calculates the hashcode inline
        """

        buf = self.fileobj.read(size)

        # running checksum
        self.hashval.update(buf)

        return buf

    def validate_hash(self):
        """
        validate that the calculated hash matches the hash uploaded in the tar file
        """
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
            size_str = str(size)

            buf = StringIO()

            curl = pycurl.Curl()

            curl.setopt(curl.PUT, True)

            mod_time = time.ctime(info.mtime)

            curl.setopt(curl.HTTPHEADER,['Last-Modified: ' + mod_time, 
                                         'Content-Type: application/octet-stream',
                                         'Content-Length: ' + size_str
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

            try:
                ret_dict = json.loads(body)
                msg = ret_dict['message']
                print msg

                bytes = int(ret_dict['total_bytes'])
                if bytes != info.size:
                    return False
            except Exception, ex:
                print ex
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
    """
    class used to hold and search metadata
    """

    meta_dict = None
    file_dict = None

    def load_meta(self, tar):
        """
        loads the metadata from a tar file into searchable structures
        """

        string = tar.extractfile('metadata.txt').read()

        self.meta_dict = json.loads(string)

        files = self.meta_dict['file']

        self.file_dict = {}

        for elem in files:
            fname = elem['fileName']
            hashcode = elem['sha1Hash']
            directory = elem['destinationDirectory']

            # force linux format
            path = directory + '/' +  fname

            self.file_dict [path] = hashcode

    def pack_meta(self):
        """
        pack metadata into a json object to pass to the metadata archive
        """

    def get_hash(self, fname):
        """
        returns the hash string for a file name
        """
        return self.file_dict[fname]


def get_clipped(fname):
    """
    returns a file path with the data separator removed
    """
    return fname.replace ('data/', '')



class TarIngester():
    """
    class to read a tar file and upload it to the metadata and file archives
    """
    fpath = ''
    server = ''
    id_start = 0

    def __init__(self, fpath, server):
        """
        constructor for TarIngester class
        """
        self.fpath = fpath
        self.server = server

    def open_tar(self):

        """ 
        seeks to the location of fpath, returns a file stream pointer and file size.
        """
        # check validity
        if not tarfile.is_tarfile(self.fpath):
            return None

        # open tar file
        try:
            tar = tarfile.open(self.fpath, 'r:')
        except tarfile.TarError:
            print "Error opening: " + self.fpath
            return None

        return tar

    def file_count(self):
        """
        retrieves the file count for a tar file
        does not count metadata.txt as that is not uploaded to the file archive
        """
        tar = self.open_tar()
        members = tar.getmembers()

        # don't count the metadata.txt file
        return len(members) - 1

    def ingest(self):
        """
        ingest a tar file into the metadata and file archives
        """
        # get the file members
        tar = self.open_tar()

        meta = MetaParser()
        meta.load_meta(tar)

        inc_id = self.id_start

         # get the file members
        members = tar.getmembers()

        for info in members:
            print info.name

            if (info.name != 'metadata.txt'):

                ingest = FileIngester(meta.get_hash(info.name), self.server, inc_id)

                ingest.upload_file_in_file(info, tar, inc_id)

                inc_id += 1


        return True