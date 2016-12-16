"""Index server unit and integration tests."""
import unittest
from ingest.orm import IngestState, BaseModel, update_state, read_state
from ingest.utils import get_unique_id, get_job_id
from ingest import tarutils
from ingest.tarutils import open_tar
from ingest.tarutils import MetaParser
from ingest.tarutils import TarIngester
from ingest.backend.tasks import ingest
from playhouse.test_utils import test_database
from peewee import SqliteDatabase
import os


# pylint: disable=too-few-public-methods


TEST_DB = SqliteDatabase(':memory:')


class IndexServerUnitTests(unittest.TestCase):
    """Index server unit and integration tests."""

    def test_load_meta(self):
        """Test sucking metadata from uploader and configuring it in a dictionary suitable to blob to meta ingest."""
        tar = open_tar('test_data/baby.tar')

        meta = MetaParser()
        meta.load_meta(tar)

    def test_tasks(self):
        job_id = get_unique_id(1, 'upload_job')

        ingest(job_id, 'test_data/baby.tar')

    def test_post_metadata(self):
        """Test sucking metadata from uploader and configuring it in a dictionary suitable to blob to meta ingest."""
        tar = open_tar('test_data/baby.tar')

        meta = MetaParser()
        meta.load_meta(tar)
        success = meta.post_metadata()

        assert(success)

    def test_ingest_tar(self):
        """Test moving individual files to the archive files are validated inline with the upload."""
        tar = open_tar('test_data/baby.tar')
        meta = MetaParser()
        meta.load_meta(tar)

        ingest = TarIngester(tar, meta)
        # validate archive process

        # if not valid:
        #     rollback()
        # success = MetaUpload()
        ingest.ingest()

    #def test_upload_file(self):
    #    """Test uploading a single file."""
    #    return
    #    for i in range(1, 20):
    #        print('from file:'.format(str(i)))
    #        upload_file('setup.py', 1)

    def test_update_state(self):
        """Test return and update of unique index."""
        return
        with test_database(TEST_DB, (BaseModel, IngestState)):
            test_object = IngestState.create(job_id=999, state='ERROR', task='unbundling',
                                             task_percent=42.3)
            self.assertEqual(test_object.job_id, 999)
            update_state(999, 'WORKING', 'validating', 33.2)
            record = read_state(999)
            self.assertEqual(record.state, 'WORKING')
            self.assertEqual(record.task, 'validating')
            # self.assertEqual(record.task_percent, 33.2)

    def test_get_job_id(self):
        """Parse the parameters for a request from the environ dictionary."""
        environ = {'QUERY_STRING': 'job_id=100'}
        job_id = get_job_id(environ)
        self.assertEqual(job_id, 100)


if __name__ == '__main__':
    unittest.main()
    print('test complete')
