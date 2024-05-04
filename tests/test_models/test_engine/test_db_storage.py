import unittest
import MySQLdb
from models import storage
from os import getenv
from models.state import State

@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', "testing for database storage engine")
class TestDBStorage(unittest.TestCase):
    """Testing the database storage engine"""

    """Set up the test environment"""
    def setUp(self):
        self.hostname = getenv('HBNB_MYSQL_HOST')
        self.user = getenv('HBNB_MYSQL_USER')
        self.passwd = getenv('HBNB_MYSQL_PWD')
        self.db = getenv('HBNB_MYSQL_DB')

    def test_storage(self):
        """Test querying the database"""
        conn = MySQLdb.connect(host=self.hostname, user=self.user,
                               passwd=self.passwd, db=self.db)
        curr = conn.cursor()
        curr.execute("SELECT COUNT(*) FROM states")
        result = curr.fetchone()[0]

        curr.execute("SELECT COUNT(*) FROM states")
        new_result = curr.fetchone()[0]
        self.assertEqual(new_result - result, 1)