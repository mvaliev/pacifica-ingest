"""
    index server unit and integration tests
"""
import unittest
from ingest_orm import IngestState, BaseModel, update_state, read_state

from ingest_utils import get_job_id, create_invalid_return, create_return_params, create_state_return, \
                         get_unique_id, receive, rename_bundle, valid_request, upload_file

from ingest_tar_utils import TarIngester

from playhouse.test_utils import test_database
from peewee import SqliteDatabase

# pylint: disable=too-few-public-methods

TEST_DB = SqliteDatabase(':memory:')

class IndexServerUnitTests(unittest.TestCase):
    """
    index server unit and integration tests
    """

    def test_ingest_tar(self):

        ingest = TarIngester('c:\\Temp\\test.tar', 'http://130.20.227.120:8067/')

        count = ingest.file_count()

        # this is where we would get a unique range of id's
        # and set the start id to the low end of the range
        ingest.id_start = 0

        ingest.ingest()

    def test_upload_file(self):
        return
        for i in range(1, 20):
            print "from file:" + str(i)
            upload_file('c:\\Temp\\index.html', 1)

    def test_update_state(self):
        """
        test return and update of unique index
        """

        with test_database(TEST_DB, (BaseModel, IngestState)):
            test_object = IngestState.create(job_id=999, state='ERROR', task='unbundling',
                                             task_percent=42.3)

            self.assertEqual(test_object.job_id, 999)

            update_state(999, 'WORKING', 'validating', 33.2)

            record = read_state(999)

            self.assertEqual(record.state, 'WORKING')
            self.assertEqual(record.task, 'validating')
            #self.assertEqual(record.task_percent, 33.2)

    def test_get_job_id(self, environ):
        """
        parse the parameters for a request from the environ dictionary
        #"""
        #environ['QUERY_STRING']
        #environ = {'QUERY_STRING':['job_id':100]}
        #job_id = get_job_id(environ)
        #self.assertEqual(job_id, 100)



if __name__ == '__main__':
    unittest.main()
    print 'test complete'
