# Air Quality Monitoring App

## Overview
This application monitors air quality using data published by Główny Inspektorat Ochrony Środowiska and retrieved via REST API https://powietrze.gios.gov.pl/pjp/content/api.
## Prerequisites
- Python 3.7+
- PyCharm IDE (recommended; PyCharm Community Edition: https://www.jetbrains.com/pycharm/download/?section=windows)

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/DariuszDzi/AirQualityApp.git
cd AirQualityApp
```
### Step 2: Set Up the Project in PyCharm
1. Open PyCharm and select File > Open.
2. Navigate to the directory where AirQualityApp project is located and open it.

#### Set Up the Virtual Environment:
1. Go to File > Settings (or PyCharm > Preferences on macOS).
2. Navigate to Project: AirQualityApp > Python Interpreter.
3. Click the gear icon and select Add.
4. Choose New Environment and set the location. Ensure the base interpreter is set to your installed Python version.
5. Click OK to create the virtual environment.

#### Install Dependencies:
1. Right-click on requirements.txt in the Project pane.
2. Select Install Requirements.

## Running the Application
1. In the Project pane, navigate to app/main_window.py.
2. Right-click on main_window.py and select Run 'main_window'.
## Running the Tests
1. Right-click on the tests directory in the Project pane.
2. Select Run 'Unittests in tests'.

## Basic functionality
1. Enter a city to look up measurement station > write either a full name of the city your looking for or first few letters. Initiate by pressing Look Up button.
2. Clear Data button > clears all data stored in the app database.
3. Analyze Data > offers a simple data analysis based on the data stored in the app database. Includes visual data plotting via Plot Data button.
