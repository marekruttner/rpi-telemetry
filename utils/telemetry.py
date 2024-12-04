import psutil
import time
import threading
import csv
import os

# Initialize variables
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'telemetry_log.csv')

# Check if log file exists, if not, create and write headers
if not os.path.isfile(log_file):
    with open(log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'CPU_Usage', 'CPU_Temp', 'RAM_Usage', 'Processes'])

def collect_telemetry():
    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        cpu_usage = psutil.cpu_percent(interval=1)

        # Get CPU temperature
        try:
            cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        except (KeyError, IndexError):
            cpu_temp = None  # Handle cases where temperature is not available

        ram_usage = psutil.virtual_memory().percent
        processes = len(psutil.pids())

        # Log data to CSV file
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, cpu_usage, cpu_temp, ram_usage, processes])

        # Sleep for a defined interval
        time.sleep(5)  # Collect data every 5 seconds
