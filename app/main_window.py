import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import logging
from app.data_fetcher import get_station_list, get_sensors_for_station, get_measurement_data
from app.db_manager import create_tables, insert_station, insert_sensor, insert_measurement, clear_data, inspect_db
from app.data_analyzer import read_data, analyze_data, plot_data
from app.frames.welcome_frame import WelcomeFrame
from app.frames.station_frame import StationFrame
from app.frames.sensor_frame import SensorFrame
from app.frames.data_analysis_frame import DataAnalysisFrame
import sqlite3

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AirQualityApp:
    """
    Main application class for the Air Quality Monitoring App.
    """
    def __init__(self, root):
        """
        Initialize the application.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Air Quality Monitoring App")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.frames = {}
        self.sensors = []
        self.selected_station = None
        self.selected_sensor = None
        self.station_list = []
        self.current_data = None

        self.db_path = self.ensure_data_directory()
        self.conn = sqlite3.connect(self.db_path)
        create_tables(self.conn)

        self.init_frames()
        self.show_frame("welcome_frame")
        self.populate_analyze_data_stations()

    def ensure_data_directory(self):
        """
        Ensure the data directory exists and return the database path.

        Returns:
            str: The path to the database file.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.abspath(os.path.join(base_dir, '..', 'data'))
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        logger.info(f"Data directory path: {data_dir}")

        db_path = os.path.join(data_dir, 'air_quality.db')
        logger.info(f"Database path: {db_path}")
        if not os.path.exists(db_path):
            with open(db_path, 'w'):
                pass  # Create an empty file if it doesn't exist
        return db_path

    def init_frames(self):
        """
        Initialize the frames of the application.
        """
        self.frames["welcome_frame"] = WelcomeFrame(self.root, self)
        self.frames["station_frame"] = StationFrame(self.root, self)
        self.frames["sensor_frame"] = SensorFrame(self.root, self)
        self.frames["data_analysis_frame"] = DataAnalysisFrame(self.root, self)

        for frame in self.frames.values():
            frame.place(x=0, y=0, relwidth=1, relheight=1)

    def show_frame(self, frame_name):
        """
        Show the specified frame.

        Args:
            frame_name (str): The name of the frame to show.
        """
        frame = self.frames[frame_name]
        frame.tkraise()

    def lookup_city(self, city_name):
        """
        Look up measurement centers in the specified city.

        Args:
            city_name (str): The name of the city to look up.
        """
        self.station_list = get_station_list()
        filtered_stations = [station for station in self.station_list if city_name in station['city']['name'].lower()]

        if not filtered_stations:
            messagebox.showinfo("No Results", f"No measurement centers found for city: {city_name}")
            return

        self.frames["station_frame"].populate_stations(filtered_stations)
        self.show_frame("station_frame")

    def on_station_select(self, index):
        """
        Handle station selection and populate sensors for the selected station.

        Args:
            index (int): The index of the selected station in the list.
        """
        self.selected_station = self.frames["station_frame"].stations[index]
        logger.info(f"Selected Station: {self.selected_station}")
        selected_station_id = self.selected_station['id']
        self.sensors = get_sensors_for_station(selected_station_id)
        if self.sensors:
            self.frames["sensor_frame"].populate_sensors(self.sensors)
            self.show_frame("sensor_frame")

    def on_sensor_select(self, index):
        """
        Handle sensor selection and display measurement data for the selected sensor.

        Args:
            index (int): The index of the selected sensor in the list.
        """
        self.selected_sensor = self.sensors[index]
        logger.info(f"Selected Sensor: {self.selected_sensor}")
        selected_sensor_id = self.selected_sensor['id']
        measurement_data = get_measurement_data(selected_sensor_id)
        if measurement_data:
            self.display_measurement_data(measurement_data)
            self.frames["sensor_frame"].show_save_button()

    def display_measurement_data(self, measurement_data):
        """
        Display measurement data for the selected sensor.

        Args:
            measurement_data (dict): Dictionary containing measurement data.
        """
        if 'values' in measurement_data:
            values = measurement_data['values']
            self.current_data = None

            for data in values:
                if data['value'] is not None:
                    if self.current_data is None:
                        self.current_data = data
                    else:
                        self.current_data.update({
                            'historical_value': data['value'],
                            'historical_value_date': data['date']
                        })
                        break

            if self.current_data:
                current_value = self.current_data['value']
                date_time = self.current_data['date']
                data_str = f"Current Value: {current_value}\nDate: {date_time}"
                if 'historical_value' in self.current_data and 'historical_value_date' in self.current_data:
                    historical_value = self.current_data['historical_value']
                    historical_date = self.current_data['historical_value_date']
                    data_str += f"\n\nHistorical Value: {historical_value}\nDate: {historical_date}"
                else:
                    data_str += "\n\nNo historical data available."
            else:
                data_str = "No data available."
        else:
            data_str = "No current data available, showing historical data if available."

        self.frames["sensor_frame"].display_measurement_data(data_str)

    def save_data(self):
        """
        Save the current measurement data to the database.
        """
        if self.current_data and self.selected_station and self.selected_sensor:
            logger.info(f"Saving data for station: {self.selected_station}, sensor: {self.selected_sensor}")
            logger.info(f"Current Data: {self.current_data}")
            insert_station(self.conn, self.selected_station)
            insert_sensor(self.conn, self.selected_sensor)
            insert_measurement(self.conn, self.selected_sensor['id'], {"values": [self.current_data]}, self.selected_station, self.selected_sensor)
            inspect_db(self.conn)  # Add a call to inspect the database contents after saving
            self.populate_analyze_data_stations()  # Refresh the stations in the data analysis frame
            messagebox.showinfo("Data Saved", "The current data has been saved to the database.")
        else:
            messagebox.showwarning("Save Error", "No data to save.")

    def clear_database(self):
        """
        Clear all data from the database.
        """
        clear_data(self.conn)
        messagebox.showinfo("Data Cleared", "All data has been cleared from the database.")

    def populate_analyze_data_stations(self):
        """
        Populate the station list for data analysis.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, stationName FROM stations")
        stations = cursor.fetchall()

        station_list = [{'id': id, 'stationName': name} for id, name in stations]
        self.frames["data_analysis_frame"].populate_stations(station_list)

    def update_sensors(self, station_id):
        """
        Update the sensor list for the selected station.

        Args:
            station_id (int): The ID of the selected station.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, paramName FROM sensors WHERE stationId=?", (station_id,))
        sensors = cursor.fetchall()

        sensor_list = [{'id': id, 'param': {'paramName': name}, 'stationId': station_id} for id, name in sensors]
        self.frames["data_analysis_frame"].populate_sensors(sensor_list)

    def analyze_data(self):
        """
        Analyze the data for the selected sensor and date range.
        """
        sensor_id = self.frames["data_analysis_frame"].get_selected_sensor_id()
        start_date = self.frames["data_analysis_frame"].get_start_date()
        end_date = self.frames["data_analysis_frame"].get_end_date()
        try:
            df = read_data(self.db_path, sensor_id)
            if not df.empty:
                if start_date:
                    df = df[df['date'] >= pd.Timestamp(start_date)]
                if end_date:
                    df = df[df['date'] <= pd.Timestamp(end_date)]
                analysis = analyze_data(df)
                self.display_analysis(analysis)
            else:
                messagebox.showinfo("No Data", "No data found for the given Sensor ID.")
        except Exception as e:
            logger.error(f"Error analyzing data: {e}")
            messagebox.showerror("Error", str(e))

    def display_analysis(self, analysis):
        """
        Display the analysis results.

        Args:
            analysis (dict): A dictionary containing analysis results.
        """
        analysis_str = f"""
        Minimum Value: {analysis['min_value']} (Date: {analysis['min_date']})
        Maximum Value: {analysis['max_value']} (Date: {analysis['max_date']})
        Average Value: {analysis['mean_value']}
        Trend: {analysis['trend']}
        """
        messagebox.showinfo("Analysis Results", analysis_str)

    def plot_data(self):
        """
        Plot the data for the selected sensor and date range.
        """
        sensor_id = self.frames["data_analysis_frame"].get_selected_sensor_id()
        start_date = self.frames["data_analysis_frame"].get_start_date()
        end_date = self.frames["data_analysis_frame"].get_end_date()
        try:
            df = read_data(self.db_path, sensor_id)
            plot_data(self.db_path, sensor_id, df, start_date, end_date)
        except Exception as e:
            logger.error(f"Error plotting data: {e}")
            messagebox.showerror("Error", str(e))

    def go_back_to_welcome(self):
        """
        Go back to the welcome screen.
        """
        self.frames["data_analysis_frame"].clear_station_combobox()
        self.frames["data_analysis_frame"].clear_sensor_and_date_comboboxes()
        self.show_frame("welcome_frame")

if __name__ == "__main__":
    root = tk.Tk()
    app = AirQualityApp(root)
    root.mainloop()
