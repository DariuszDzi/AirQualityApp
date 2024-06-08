import requests
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_station_list():
    """
    Fetch the list of all stations from the API.

    Returns:
        list: A list of dictionaries containing station data, or None if an error occurs.
    """
    try:
        response = requests.get('https://api.gios.gov.pl/pjp-api/rest/station/findAll')
        response.raise_for_status()
        stations = response.json()
        for station in stations:
            station['id'] = int(station['id'])
            station['gegrLat'] = float(station['gegrLat'])
            station['gegrLon'] = float(station['gegrLon'])
        return stations
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching station list: {e}")
        return None

def get_sensors_for_station(station_id):
    """
    Fetch the list of sensors for a specific station.

    Args:
        station_id (int): The ID of the station.

    Returns:
        list: A list of dictionaries containing sensor data, or None if an error occurs.
    """
    try:
        url = f'https://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}'
        response = requests.get(url)
        response.raise_for_status()
        sensors = response.json()
        for sensor in sensors:
            sensor['id'] = int(sensor['id'])
            sensor['stationId'] = int(sensor['stationId'])
        return sensors
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching sensors for station {station_id}: {e}")
        return None

def get_measurement_data(sensor_id):
    """
    Fetch measurement data for a specific sensor.

    Args:
        sensor_id (int): The ID of the sensor.

    Returns:
        dict: A dictionary containing measurement data, or None if an error occurs.
    """
    try:
        url = f'https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Raw measurement data: {data}")
        values = []
        for value in data['values']:
            if value['value'] is not None:
                measurement = {
                    'date': value['date'],
                    'value': float(value['value']),
                }
                if 'historical_value' in value:
                    measurement['historical_value'] = float(value['historical_value'])
                if 'historical_value_date' in value:
                    measurement['historical_value_date'] = value['historical_value_date']
                values.append(measurement)
        return {'values': values}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching measurement data for sensor {sensor_id}: {e}")
        return None

def get_air_quality_index(station_id):
    """
    Fetch the air quality index for a specific station.

    Args:
        station_id (int): The ID of the station.

    Returns:
        dict: A dictionary containing air quality index data, or None if an error occurs.
    """
    try:
        url = f'https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{station_id}'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching air quality index for station {station_id}: {e}")
        return None
