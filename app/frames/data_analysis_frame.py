import tkinter as tk
from tkinter import ttk
from tkinter import Label, Button
import sqlite3
import os
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataAnalysisFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        back_button = ttk.Button(self, text="Back to Main Menu", command=self.controller.go_back_to_welcome)
        back_button.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        Label(self, text="Select Station:").grid(row=1, column=0, padx=10, pady=10)
        self.station_combobox = ttk.Combobox(self, width=50)
        self.station_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.station_combobox.bind("<<ComboboxSelected>>", self.on_station_selected)

        Label(self, text="Select Sensor:").grid(row=2, column=0, padx=10, pady=10)
        self.sensor_combobox = ttk.Combobox(self, width=50)
        self.sensor_combobox.grid(row=2, column=1, padx=10, pady=10)
        self.sensor_combobox.bind("<<ComboboxSelected>>", self.on_sensor_selected)

        Label(self, text="Start Date:").grid(row=3, column=0, padx=10, pady=10)
        self.start_date_combobox = ttk.Combobox(self, state='readonly', width=50)
        self.start_date_combobox.grid(row=3, column=1, padx=10, pady=10)

        Label(self, text="End Date:").grid(row=4, column=0, padx=10, pady=10)
        self.end_date_combobox = ttk.Combobox(self, state='readonly', width=50)
        self.end_date_combobox.grid(row=4, column=1, padx=10, pady=10)

        analyze_button = Button(self, text="Analyze Data", command=self.controller.analyze_data)
        analyze_button.grid(row=5, column=0, padx=10, pady=10)

        plot_button = Button(self, text="Plot Data", command=self.controller.plot_data)
        plot_button.grid(row=5, column=1, padx=10, pady=10)

    def on_station_selected(self, event):
        self.clear_sensor_and_date_comboboxes()
        station_id = self.station_combobox.get().split(" - ")[0]
        self.controller.update_sensors(station_id)

    def on_sensor_selected(self, event):
        sensor_id = self.sensor_combobox.get().split(" - ")[0]
        self.update_date_range(sensor_id)

    def populate_stations(self, stations):
        station_names = [f"{station['id']} - {station['stationName']}" for station in stations]
        self.station_combobox['values'] = station_names

    def populate_sensors(self, sensors):
        sensor_names = [f"{sensor['id']} - {sensor['param']['paramName']}" for sensor in sensors]
        self.sensor_combobox['values'] = sensor_names

    def update_date_range(self, sensor_id):
        db_path = self.controller.db_path
        logger.info(f"Database path in DataAnalysisFrame: {db_path}")
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found at {db_path}")

        conn = sqlite3.connect(db_path)
        query = f'''
        SELECT date FROM measurements WHERE sensorId = {sensor_id}
        UNION
        SELECT historical_value_date AS date FROM measurements WHERE sensorId = {sensor_id}
        ORDER BY date
        '''
        dates = conn.execute(query).fetchall()
        conn.close()

        date_list = [date[0] for date in dates if date[0] is not None]
        self.start_date_combobox['values'] = date_list
        self.end_date_combobox['values'] = date_list

        if date_list:
            self.start_date_combobox.set(date_list[0])
            self.end_date_combobox.set(date_list[-1])

    def get_selected_sensor_id(self):
        return self.sensor_combobox.get().split(" - ")[0]

    def get_start_date(self):
        return self.start_date_combobox.get()

    def get_end_date(self):
        return self.end_date_combobox.get()

    def clear_sensor_and_date_comboboxes(self):
        self.sensor_combobox.set('')
        self.sensor_combobox['values'] = []
        self.start_date_combobox.set('')
        self.start_date_combobox['values'] = []
        self.end_date_combobox.set('')
        self.end_date_combobox['values'] = []

    def clear_station_combobox(self):
        self.station_combobox.set('')
        # Do not clear the 'values' attribute to retain the list of stations
