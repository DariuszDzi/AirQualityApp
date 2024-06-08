import sqlite3
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS stations (
                     id INTEGER PRIMARY KEY,
                     stationName TEXT,
                     city TEXT,
                     longitude REAL,
                     latitude REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS sensors (
                     id INTEGER PRIMARY KEY,
                     stationId INTEGER,
                     paramName TEXT,
                     FOREIGN KEY(stationId) REFERENCES stations(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS measurements (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     sensorId INTEGER,
                     stationId INTEGER,
                     paramName TEXT,
                     stationName TEXT,
                     value REAL,
                     date TEXT,
                     historical_value REAL,
                     historical_value_date TEXT,
                     UNIQUE(sensorId, date),
                     FOREIGN KEY(sensorId) REFERENCES sensors(id),
                     FOREIGN KEY(stationId) REFERENCES stations(id))''')
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error creating tables: {e}")

def insert_station(conn, station):
    try:
        c = conn.cursor()
        logger.info(f"Inserting station: {station}")
        c.execute('''INSERT OR IGNORE INTO stations (id, stationName, city, longitude, latitude)
                     VALUES (?, ?, ?, ?, ?)''',
                  (station['id'], station['stationName'], station['city']['name'],
                   station['gegrLon'], station['gegrLat']))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error inserting station: {e}")

def insert_sensor(conn, sensor):
    try:
        c = conn.cursor()
        logger.info(f"Inserting sensor: {sensor}")
        c.execute('''INSERT OR IGNORE INTO sensors (id, stationId, paramName)
                     VALUES (?, ?, ?)''',
                  (sensor['id'], sensor['stationId'], sensor['param']['paramName']))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error inserting sensor: {e}")

def insert_measurement(conn, sensor_id, measurement_data, station, sensor):
    try:
        c = conn.cursor()
        logger.info(f"Inserting measurement for sensor_id {sensor_id}: {measurement_data}")
        for value in measurement_data['values']:
            logger.info(f"Processing value: {value}")
            if value['value'] is not None:
                logger.info(f"Inserting value: {value['value']} at {value['date']} for station {station['id']}, sensor {sensor_id}")
                historical_value = value.get('historical_value')
                historical_value_date = value.get('historical_value_date')
                c.execute('''INSERT OR REPLACE INTO measurements (sensorId, stationId, paramName, stationName, value, date, historical_value, historical_value_date)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                          (sensor_id, station['id'], sensor['param']['paramName'], station['stationName'],
                           value['value'], value['date'], historical_value, historical_value_date))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error inserting measurement: {e}")

def clear_data(conn):
    try:
        c = conn.cursor()
        c.execute('DELETE FROM measurements')
        c.execute('DELETE FROM sensors')
        c.execute('DELETE FROM stations')
        conn.commit()
        logger.info("All data has been cleared from the database.")
    except sqlite3.Error as e:
        logger.error(f"Error clearing data: {e}")

def inspect_db(conn):
    try:
        c = conn.cursor()
        logger.info("Inspecting database contents...")
        for table in ['stations', 'sensors', 'measurements']:
            logger.info(f"Contents of {table} table:")
            c.execute(f"SELECT * FROM {table}")
            rows = c.fetchall()
            for row in rows:
                logger.info(row)
    except sqlite3.Error as e:
        logger.error(f"Error inspecting database: {e}")
