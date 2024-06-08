from tkinter import ttk
from tkinter import messagebox

class WelcomeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        welcome_label = ttk.Label(self, text="Welcome to the Air Quality Monitoring App!", font=("Helvetica", 16))
        welcome_label.pack(padx=10, pady=10)

        city_label = ttk.Label(self, text="Enter a city to look up measurement station:")
        city_label.pack(padx=10, pady=5)

        self.city_entry = ttk.Entry(self, width=30)
        self.city_entry.pack(padx=10, pady=5)

        lookup_button = ttk.Button(self, text="Look Up", command=self.lookup_city)
        lookup_button.pack(padx=10, pady=10)

        clear_data_button = ttk.Button(self, text="Clear Data", command=self.clear_database)
        clear_data_button.pack(padx=10, pady=10)

        analyze_data_button = ttk.Button(self, text="Analyze Data", command=self.switch_to_data_analysis)
        analyze_data_button.pack(padx=10, pady=10)

    def lookup_city(self):
        city_name = self.city_entry.get().strip().lower()
        if not city_name:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        self.controller.lookup_city(city_name)

    def clear_database(self):
        self.controller.clear_database()

    def switch_to_data_analysis(self):
        self.controller.show_frame("data_analysis_frame")
