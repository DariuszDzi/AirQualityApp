import unittest
import tkinter as tk
from app.main_window import AirQualityApp

class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = AirQualityApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initial_setup(self):
        self.root.update_idletasks()  # Ensure geometry is updated
        width_height = self.app.root.geometry().split('+')[0]
        self.assertEqual(width_height, "800x600")

    def test_frames_exist(self):
        self.assertIn("welcome_frame", self.app.frames)
        self.assertIn("station_frame", self.app.frames)
        self.assertIn("sensor_frame", self.app.frames)
        self.assertIn("data_analysis_frame", self.app.frames)

if __name__ == '__main__':
    unittest.main()
