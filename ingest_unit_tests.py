"""
    index server unit and integration tests
"""
import unittest
from ingest_orm import IngestState, BaseModel, update_state, read_state


from playhouse.test_utils import test_database
from peewee import SqliteDatabase

# pylint: disable=too-few-public-methods

TEST_DB = SqliteDatabase(':memory:')

class IndexServerUnitTests(unittest.TestCase):
    """
    index server unit and integration tests
    """
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



if __name__ == '__main__':
    unittest.main()
    print 'test complete'
