import unittest
from unittest.mock import patch, Mock
from app.data_fetcher import get_station_list, get_sensors_for_station, get_measurement_data

class TestDataFetcher(unittest.TestCase):

    @patch('app.data_fetcher.requests.get')
    def test_get_station_list(self, mock_requests_get):
        # Mock the requests.get call within get_station_list
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'id': 1,
                'stationName': 'Test Station',
                'city': {'name': 'Test City'},
                'gegrLon': 10.0,
                'gegrLat': 20.0
            }
        ]
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        stations = get_station_list()
        self.assertEqual(len(stations), 1)
        self.assertEqual(stations[0]['stationName'], 'Test Station')

    @patch('app.data_fetcher.requests.get')
    def test_get_sensors_for_station(self, mock_requests_get):
        # Mock the requests.get call within get_sensors_for_station
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 1, 'param': {'paramName': 'PM2.5'}, 'stationId': 1}
        ]
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        sensors = get_sensors_for_station(1)
        self.assertEqual(len(sensors), 1)
        self.assertEqual(sensors[0]['param']['paramName'], 'PM2.5')

    @patch('app.data_fetcher.requests.get')
    def test_get_measurement_data(self, mock_requests_get):
        # Mock the requests.get call within get_measurement_data
        mock_response = Mock()
        mock_response.json.return_value = {
            'values': [{'value': 10, 'date': '2022-01-01T00:00:00Z'}]
        }
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        measurement_data = get_measurement_data(1)
        self.assertEqual(len(measurement_data['values']), 1)
        self.assertEqual(measurement_data['values'][0]['value'], 10)

if __name__ == '__main__':
    unittest.main()
