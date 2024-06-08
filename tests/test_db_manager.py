import unittest
import sqlite3
from app.db_manager import create_tables, insert_station, insert_sensor, insert_measurement, clear_data, inspect_db

class TestDBManager(unittest.TestCase):

    def setUp(self):
        """Set up an in-memory SQLite database for testing."""
        self.conn = sqlite3.connect(':memory:')
        create_tables(self.conn)

    def tearDown(self):
        """Tear down the in-memory database after each test."""
        self.conn.close()

    def test_create_tables(self):
        """Test the creation of tables."""
        c = self.conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stations'")
        self.assertIsNotNone(c.fetchone(), "Stations table should exist")
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sensors'")
        self.assertIsNotNone(c.fetchone(), "Sensors table should exist")
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='measurements'")
        self.assertIsNotNone(c.fetchone(), "Measurements table should exist")

    def test_insert_station(self):
        """Test inserting a station into the database."""
        station = {
            'id': 1,
            'stationName': 'Test Station',
            'city': {'name': 'Test City'},
            'gegrLon': 10.0,
            'gegrLat': 20.0
        }
        insert_station(self.conn, station)
        c = self.conn.cursor()
        c.execute("SELECT * FROM stations WHERE id = 1")
        result = c.fetchone()
        self.assertIsNotNone(result, "Station should be inserted")

    def test_insert_sensor(self):
        """Test inserting a sensor into the database."""
        station = {
            'id': 1,
            'stationName': 'Test Station',
            'city': {'name': 'Test City'},
            'gegrLon': 10.0,
            'gegrLat': 20.0
        }
        insert_station(self.conn, station)
        sensor = {
            'id': 1,
            'stationId': 1,
            'param': {'paramName': 'PM2.5'}
        }
        insert_sensor(self.conn, sensor)
        c = self.conn.cursor()
        c.execute("SELECT * FROM sensors WHERE id = 1")
        result = c.fetchone()
        self.assertIsNotNone(result, "Sensor should be inserted")

    def test_insert_measurement(self):
        """Test inserting a measurement into the database."""
        station = {
            'id': 1,
            'stationName': 'Test Station',
            'city': {'name': 'Test City'},
            'gegrLon': 10.0,
            'gegrLat': 20.0
        }
        insert_station(self.conn, station)
        sensor = {
            'id': 1,
            'stationId': 1,
            'param': {'paramName': 'PM2.5'}
        }
        insert_sensor(self.conn, sensor)
        measurement_data = {
            'values': [
                {'value': 15.5, 'date': '2024-06-01', 'historical_value': None, 'historical_value_date': None}
            ]
        }
        insert_measurement(self.conn, 1, measurement_data, station, sensor)
        c = self.conn.cursor()
        c.execute("SELECT * FROM measurements WHERE sensorId = 1 AND date = '2024-06-01'")
        result = c.fetchone()
        self.assertIsNotNone(result, "Measurement should be inserted")

    def test_clear_data(self):
        """Test clearing all data from the database."""
        station = {
            'id': 1,
            'stationName': 'Test Station',
            'city': {'name': 'Test City'},
            'gegrLon': 10.0,
            'gegrLat': 20.0
        }
        insert_station(self.conn, station)
        clear_data(self.conn)
        c = self.conn.cursor()
        c.execute("SELECT * FROM stations")
        result = c.fetchall()
        self.assertEqual(len(result), 0, "All data should be cleared")

    def test_inspect_db(self):
        """Test inspecting the contents of the database."""
        station = {
            'id': 1,
            'stationName': 'Test Station',
            'city': {'name': 'Test City'},
            'gegrLon': 10.0,
            'gegrLat': 20.0
        }
        insert_station(self.conn, station)
        sensor = {
            'id': 1,
            'stationId': 1,
            'param': {'paramName': 'PM2.5'}
        }
        insert_sensor(self.conn, sensor)
        measurement_data = {
            'values': [
                {'value': 15.5, 'date': '2024-06-01', 'historical_value': None, 'historical_value_date': None}
            ]
        }
        insert_measurement(self.conn, 1, measurement_data, station, sensor)
        # This test simply runs the inspect_db function to ensure no exceptions are raised.
        inspect_db(self.conn)

if __name__ == '__main__':
    unittest.main()
