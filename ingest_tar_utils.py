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
    file_id = 0
    recorded_hash = ''
    hashval = None
    server = ''

    def __init__(self, hashcode, server, file_id):
        """
        constructor for FileIngester class
        """

        self.hashval = hashlib.sha1()
        self.recorded_hash = hashcode
        self.server = server
        self.file_id = file_id

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

    def upload_file_in_file(self, info, tar):
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

            curl.setopt(curl.URL, self.server + str(self.file_id))
            curl.setopt(curl.WRITEDATA, buf)

            curl.perform()
            curl.close()

            self.fileobj.close()

            body = buf.getvalue()

            try:
                ret_dict = json.loads(body)
                msg = ret_dict['message']
                print msg

                size = int(ret_dict['total_bytes'])
                if size != info.size:
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

    # entire metadata 
    meta = None

    # a map of filenames to hashcodes
    files = None

    startID = -999
    transactionID = -999

    def __init__(self, transactionID, startID):
        """
        constructor
        """
        self.transactionID = transactionID
        self.startID = startID

    def load_meta(self, tar):
        """
        loads the metadata from a tar file into searchable structures
        """

        string = tar.extractfile('metadata.txt').read()

        received = json.loads(string)

        received_eus = received['eusInfo']

        transaction = {'ID':self.transactionID,
                     'submitter': 'do not have this',
                     'proposal':received_eus['proposalID'],
                     'instrument':received_eus['instrumentId']}

        groups = received_eus['groups']

        packupload = {}
        for element in groups:
            value = element['name']
            key = element['type']
            packupload[key] = value

        transaction['user_search_meta'] = packupload

        id = self.startID
        recieved_files = received['file']
        files = {}

        for elem in recieved_files:
            fname = elem['fileName']
            hashcode = elem['sha1Hash']
            directory = elem['destinationDirectory']

            # force linux format
            path = directory + '/' +  fname

            # we don't upload the metadata file
            if path == 'metadata.txt':
                continue

            # open the file in the tar to get the file info
            member = tar.getmember(path)

            file_element = {'name': path,
                            'subdir': directory,
                            'hash':'sha1:' + hashcode, 
                            'vtime': '',
                            'mtime': member.mtime,
                            'verified': False,
                            'size': member.size,
                            'transaction': self.transactionID}

            files[id] = file_element;
            id+=1

        self.files = files

        self.meta = {}
        self.meta['transaction'] = transaction
        self.meta['files'] = files


    def get_hash(self, id):
        """
        returns the hash string for a file name
        """
        file_element = self.files[id]
        
        #remove filetype
        hash = file_element['hash'].replace('sha1:', '')

        return hash

    def get_fname(self, id):
        """
        returns the hash string for a file name
        """
        file_element = self.files[id]
        
        #remove filetype
        hash = file_element['name']

        return hash


class TarIngester():
    """
    class to read a tar file and upload it to the metadata and file archives
    """
    tar = None
    meta = None
    server = ''
    startID = -999
    transactionID = -999

    def __init__(self, tar, meta, server):
        """
        constructor for TarIngester class
        """
        self.tar = tar
        self.meta = meta
        self.server = server

    def ingest(self):
        """
        ingest a tar file into the metadata and file archives
        """

        keys = self.meta.files.keys()

        for id in keys:

            hash = self.meta.get_hash(id)
            name = self.meta.get_fname(id)

            info = self.tar.getmember(name)

            print info.name

            ingest = FileIngester(hash, self.server, id)

            ingest.upload_file_in_file(info, self.tar)

        return True

def get_clipped(fname):
    """
    returns a file path with the data separator removed
    """
    return fname.replace('data/', '')

def open_tar(fpath):

    """
    seeks to the location of fpath, returns a file stream pointer and file size.
    """
    # check validity
    if not tarfile.is_tarfile(fpath):
        return None

    # open tar file
    try:
        tar = tarfile.open(fpath, 'r:')
    except tarfile.TarError:
        print "Error opening: " + fpath
        return None

    return tar

def file_count(tar):
    """
    retrieves the file count for a tar file
    does not count metadata.txt as that is not uploaded to the file archive
    """
    members = tar.getmembers()

    # don't count the metadata.txt file
    return len(members) - 1
