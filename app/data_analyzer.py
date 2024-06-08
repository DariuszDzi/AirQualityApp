import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def read_data(db_path, sensor_id):
    """
    Read data from the database for a specific sensor.

    Args:
        db_path (str): Path to the database file.
        sensor_id (int): The ID of the sensor.

    Returns:
        DataFrame: A pandas DataFrame containing combined current and historical data.
    """
    conn = sqlite3.connect(db_path)
    query = f'''
    SELECT date, value, historical_value, historical_value_date
    FROM measurements
    WHERE sensorId = {sensor_id}
    '''
    df = pd.read_sql_query(query, conn, parse_dates=['date', 'historical_value_date'])
    conn.close()

    historical_df = df[['historical_value_date', 'historical_value']].rename(
        columns={'historical_value_date': 'date', 'historical_value': 'value'}
    ).dropna()

    combined_df = pd.concat([df[['date', 'value']], historical_df], ignore_index=True).dropna().sort_values(by='date')
    return combined_df

def get_sensor_info(db_path, sensor_id):
    """
    Get sensor information from the database.

    Args:
        db_path (str): Path to the database file.
        sensor_id (int): The ID of the sensor.

    Returns:
        tuple: A tuple containing the parameter name and station name.
    """
    conn = sqlite3.connect(db_path)
    query = '''
    SELECT sensors.paramName, stations.stationName
    FROM sensors
    JOIN stations ON sensors.stationId = stations.id
    WHERE sensors.id = ?
    '''
    result = conn.execute(query, (sensor_id,)).fetchone()
    conn.close()
    return result

def analyze_data(df):
    """
    Analyze the data to extract minimum, maximum, and mean values, as well as the trend.

    Args:
        df (DataFrame): A pandas DataFrame containing the data to be analyzed.

    Returns:
        dict: A dictionary containing analysis results.
    """
    analysis = {}
    if not df.empty:
        analysis['min_value'] = df['value'].min()
        analysis['min_date'] = df.loc[df['value'] == analysis['min_value'], 'date'].iloc[0]
        analysis['max_value'] = df['value'].max()
        analysis['max_date'] = df.loc[df['value'] == analysis['max_value'], 'date'].iloc[0]
        analysis['mean_value'] = df['value'].mean()
        analysis['trend'] = 'Increasing' if df['value'].iloc[-1] > df['value'].iloc[0] else 'Decreasing'
    return analysis

def plot_data(db_path, sensor_id, df, start_date=None, end_date=None):
    """
    Plot the data over time, including current and historical values, with annotations for min, max, and mean values.

    Args:
        db_path (str): Path to the database file.
        sensor_id (int): The ID of the sensor.
        df (DataFrame): A pandas DataFrame containing the data to be plotted.
        start_date (str, optional): Start date for filtering the data.
        end_date (str, optional): End date for filtering the data.
    """
    if start_date:
        df = df[df['date'] >= start_date]
    if end_date:
        df = df[df['date'] <= end_date]

    sensor_info = get_sensor_info(db_path, sensor_id)
    if sensor_info:
        param_name, station_name = sensor_info
    else:
        param_name, station_name = "Unknown Sensor", "Unknown Station"

    current_df = df[df['date'].isin(df['date'].unique())]
    historical_df = df[~df['date'].isin(current_df['date'].unique())]

    plt.figure(figsize=(12, 8))

    plt.plot(current_df['date'], current_df['value'], marker='o', linestyle='-', color='b', label='Current Values')

    if not historical_df.empty:
        plt.plot(historical_df['date'], historical_df['value'], marker='x', linestyle='--', color='r', label='Historical Values')

    analysis = analyze_data(df)
    if analysis:
        offset = (df['value'].max() - df['value'].min()) * 0.05
        min_offset = -offset if analysis['min_value'] > df['value'].min() + offset else offset
        max_offset = offset * 2 if analysis['max_value'] < df['value'].max() - offset else -offset * 2

        plt.annotate(f"Min: {analysis['min_value']}\non {analysis['min_date']:%Y-%m-%d %H:%M}",
                     xy=(analysis['min_date'], analysis['min_value']),
                     xytext=(analysis['min_date'], analysis['min_value'] + min_offset),
                     arrowprops=dict(facecolor='black', arrowstyle='->'),
                     bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='white'))
        plt.annotate(f"Max: {analysis['max_value']}\non {analysis['max_date']:%Y-%m-%d %H:%M}",
                     xy=(analysis['max_date'], analysis['max_value']),
                     xytext=(analysis['max_date'], analysis['max_value'] + max_offset),
                     arrowprops=dict(facecolor='black', arrowstyle='->'),
                     bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='white'))
        mean_value = analysis['mean_value']
        plt.axhline(y=mean_value, color='g', linestyle='-', label=f'Mean Value: {mean_value:.2f}')

    plt.title(f'Data Over Time\n{param_name} at {station_name}', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.legend()
    plt.grid(True)

    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
