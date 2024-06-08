import tkinter as tk
from tkinter import ttk
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SensorFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sensors = []
        self.create_widgets()

    def create_widgets(self):
        self.sensor_frame_left = ttk.Frame(self)
        self.sensor_frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        sensor_label = ttk.Label(self.sensor_frame_left, text="Choose a sensor:")
        sensor_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.sensor_listbox = tk.Listbox(self.sensor_frame_left, width=50, height=10)
        self.sensor_listbox.grid(row=1, column=0, rowspan=4, padx=10, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)

        select_sensor_button = ttk.Button(self.sensor_frame_left, text="Select Sensor", command=self.on_sensor_select)
        select_sensor_button.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)

        self.data_frame = ttk.Frame(self)
        self.data_frame.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")

        self.sensor_data_label = ttk.Label(self.data_frame, text="", anchor="nw", justify="left")
        self.sensor_data_label.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the Back and Save Data buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        back_button = ttk.Button(button_frame, text="Back", command=self.go_back)
        back_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.save_data_button = ttk.Button(button_frame, text="Save Data", command=self.controller.save_data)
        self.save_data_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        self.save_data_button.grid_remove()  # Hide initially

    def populate_sensors(self, sensors):
        self.sensor_listbox.delete(0, tk.END)
        self.sensors = sensors
        for sensor in sensors:
            self.sensor_listbox.insert(tk.END, f"{sensor['id']} - {sensor['param']['paramName']}")

    def on_sensor_select(self):
        selected_index = self.sensor_listbox.curselection()
        if selected_index:
            sensor = self.sensors[selected_index[0]]
            self.controller.on_sensor_select(selected_index[0])
            logger.info(f"Sensor Selected: {sensor}")

    def display_measurement_data(self, data_str):
        self.sensor_data_label.config(text=data_str)

    def show_save_button(self):
        self.save_data_button.grid()

    def go_back(self):
        self.controller.show_frame("station_frame")
