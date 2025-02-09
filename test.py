import unittest
from unittest.mock import MagicMock
from user import Database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Mock the database connection and cursor
        self.db_mock = MagicMock()
        self.database = Database('test.db')
        self.database.conn = self.db_mock
        self.database.cursor = self.db_mock.cursor()
        
    def test_insert_user(self):
        # Test insert_user method
        self.db_mock.cursor().lastrowid = 1  # Mock the lastrowid value
        user_id = self.database.insert_user('John Doe', 30)
        self.db_mock.cursor().execute.assert_called_with('INSERT INTO users (name, age) VALUES (?, ?)', ('John Doe', 30))
        self.assertEqual(user_id, 1)
        
    def test_get_user(self):
        # Mock the response of get_user method
        self.db_mock.cursor().fetchone.return_value = (1, 'John Doe', 30)
        user = self.database.get_user(1)
        self.db_mock.cursor().execute.assert_called_with('SELECT * FROM users WHERE user_id = ?', (1,))
        self.assertEqual(user, (1, 'John Doe', 30))
        
    def test_update_user(self):
        # Test update_user method
        self.db_mock.cursor().rowcount = 1  # Mock rowcount to simulate an updated row
        self.database.update_user(1, 'Jane Doe', 28)
        self.db_mock.cursor().execute.assert_called_with('UPDATE users SET name = ?, age = ? WHERE user_id = ?', ('Jane Doe', 28, 1))
        
    def test_delete_user(self):
        # Test delete_user method
        self.db_mock.cursor().rowcount = 1  # Mock rowcount to simulate a deleted row
        self.database.delete_user(1)
        self.db_mock.cursor().execute.assert_called_with('DELETE FROM users WHERE user_id = ?', (1,))

if __name__ == '__main__':
    unittest.main()
