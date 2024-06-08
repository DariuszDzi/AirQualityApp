import tkinter as tk
from tkinter import ttk
import logging

logger = logging.getLogger(__name__)

class StationFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.stations = []
        self.create_widgets()

    def create_widgets(self):
        station_label = ttk.Label(self, text="Choose a station:")
        station_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.station_listbox = tk.Listbox(self, width=50, height=10)
        self.station_listbox.grid(row=1, column=0, rowspan=4, padx=10, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)

        select_station_button = ttk.Button(self, text="Select Station", command=self.on_station_select)
        select_station_button.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)

        back_button = ttk.Button(self, text="Back", command=self.go_back)
        back_button.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

    def populate_stations(self, stations):
        self.station_listbox.delete(0, tk.END)
        self.stations = stations
        for station in stations:
            self.station_listbox.insert(tk.END, f"{station['id']} - {station['stationName']}")

    def on_station_select(self):
        selected_index = self.station_listbox.curselection()
        if selected_index:
            station = self.stations[selected_index[0]]
            self.controller.on_station_select(selected_index[0])
            logger.info(f"Station Selected: {station}")

    def go_back(self):
        self.controller.show_frame("welcome_frame")
