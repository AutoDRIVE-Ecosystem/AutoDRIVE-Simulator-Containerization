import csv
import os
from datetime import datetime
import requests

########################################################
#
# HPC Framework Data Logging Module
#
########################################################


# log_entry() --> Function to collect required metrics from AutoDRIVE & write to a row in csv
#   - currently desired metrics are hard coded into the function definition, this should be changed to accept them as parameters (or maybe dynamically figure them out?)
# arg: ...
#   each argument directly corresponds to a value recorded from autodrive.py/rzr_aeb.py and equates to one row of data
def log_entry(model, weather_id, time_of_day, label, confidence, size, AEB, DTC, collision_count, position, orientation_euler_angles, throttle, steering, brake, handbrake):
    csv_filename = 'metrics.csv'
    header = ['Timestamp', "Time of Day (min)", "Weather ID (#)", "Model", "Label", "Confidence (%)", "Size (px^2)", "AEB (bool)", "DTC (m)", "Throttle (%)", "Steering (%)", "Brake (%)", "Handbrake (%)", "PosX (m)", "PosY (m)", "PosZ (m)", "RotX (rad)", "RotY (rad)", "RotZ (rad)", "Collisions (#)"]
    # Check if the file exists
    file_exists = os.path.isfile(csv_filename)

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Open the CSV file in append mode
    with open(csv_filename, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write header if the file is newly created
        if not file_exists:
            writer.writerow(header)

        # Write event, data, and timestamp to the CSV file
        
        writer.writerow([timestamp, time_of_day, weather_id, model, label, confidence, size, AEB, DTC, throttle, steering, brake, handbrake, position[0], position[1], position[2], orientation_euler_angles[0], orientation_euler_angles[1], orientation_euler_angles[2], collision_count])

# send_metrics() --> function to send recorded metrics.csv to the control server via an open endpoint
#   - This function can either be called remotely by the control server via kubectl exec or locally in the simulator script once a test case
#       has finished.
def send_metrics():
    # Specify the file path
    file_path = "/app/metrics.csv"

    try:
        # Open the CSV file and read its contents
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            data = [row for row in csv_reader]
        
        # Prepare the data to be sent in the POST request
        payload = {'data': data}

        # Send the data to the server endpoint
        response = requests.post('http://10.128.199.51:30837/database', json=payload)

        # Check for a successful response
        if response.status_code == 200:
            print("Data sent successfully:", response.text)
        else:
            print("Failed to send data. Status code:", response.status_code)

    except Exception as e:
        print("Error reading or sending CSV file:", e)