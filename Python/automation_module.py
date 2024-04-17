import subprocess
import csv
import re
import k8api
import requests
import time
import os
import configparser

##############################################################################
#
#   HPC FRAMEWORK AUTOMATION MODULE
#
##############################################################################

# Configure Parameters
config = configparser.ConfigParser()

# Read the .ini file
config.read('config.ini')

# Extract values
NAMESPACE = config['DEFAULT']['namespace']
DEPLOYMENT = config['DEFAULT']['deployment']
SIMULATION_CONTAINER = config['DEFAULT']['simulator_container']
API_CONTAINER = config['DEFAULT']['api_container']
SERVER_IP = config['DEFAULT']['server_ip']


# run_kubectl_command() --> helper/wrapper function to run commands with kubectl
#       Used to spin up subprocesses which use the systems existing kubectl configuration
#       A similar behavior can be achieved with the kubernetes python client, but this approach creates less network errors
# arg command: string storing command to run in the subprocess
def run_kubectl_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return None

# parse_and_save_to_csv() --> helper function that accepts, processes, and outputs to a csv cluster wide metric data and gpu metric data.
# arg top_output: captured output of 'kubectl top nodes' to be processed
# arg gpu_out: captured output of gpu data (from nvidia-smi inside a gpu enabled pod)
# arg csv_filename: desired filename for csv file
def parse_and_save_to_csv(top_output, gpu_out, csv_filename):
    # Define the header for the CSV file
    header = ["Node Name", "CPU Cores", "CPU Usage (%)", "Memory Usage (MiB)", "Memory Usage (%)", "GPU Index", "GPU Name", "GPU Usage (%)", "GPU Memory Usage (%)", "GPU Memory Total (MiB)", "GPU Memory Usage (MiB)", "GPU Power Usage (W)"]

    # Regular expression pattern for extracting values from each line
    pattern = re.compile(r'(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')

    # List to store parsed data for each line
    parsed_data = []
    gpu_data = gpu_out

    # Iterate through each line in the output !!! Need to change this to search for all nodes !!!
    for line in top_output.split('\n')[1:]:
        match = pattern.match(line)
        if match:
            name, cpu_cores, cpu_percent, memory, memory_percent = match.groups()
            if(name != 'tw0002.dev.rcd.clemson.edu' and name in gpu_data.keys()):
                parsed_data.append([name, cpu_cores, cpu_percent, memory, memory_percent, gpu_data[name][0], gpu_data[name][1], gpu_data[name][2], gpu_data[name][3], gpu_data[name][4], gpu_data[name][5], gpu_data[name][6]])

    # Save the parsed data to a CSV file  
    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        if not file_exists:
            writer.writerow(header)
        
        writer.writerows(parsed_data)


# Function to Record and log resource metrics
# record_resource_metrics() --> function to collect cluster wide resources, 
#    then pass them along to be processed and saved. Called periodically by watch_simulation()
# arg filename: desired filename for csv file
# arg pods: list of current pods (passed to avoid overloading k8 api)
def record_resource_metrics(filename, pods):

    # Collect cluster wide metrics (CPU, Memory, Node info) from kubectl
    kubectl_command = "kubectl top nodes -n " + NAMESPACE
    top_output = run_kubectl_command(kubectl_command)
    # Collect gpu metrics
    gpu_data = record_gpu(pods)

    if top_output:
        # parse resource metrics & save them to a csv
        parse_and_save_to_csv(top_output, gpu_data, filename)
    else:
        print("Failed to retrieve kubectl top nodes data.")

# record_gpu() --> Helper Function to record gpu metrics, called in parse_and_save_to_csv fxn
#      gpu is recorded separately from cpu since it requires running nvidia-smi inside of a running pod
# arg pods: list of current pods
def record_gpu(pods):
    podnames = []
    nodes = []
    for pod in pods:
        if DEPLOYMENT in pod[0] and pod[1] not in nodes:
            podnames.append((pod[0], pod[1]))
            nodes.append(pod[1])

    ##### Un-comment to use the kubernetes python client rather than python subprocesses #####
    # command = "nvidia-smi --query-gpu=index,name,utilization.gpu,utilization.memory,memory.total,memory.used,power.draw --format=csv,noheader"
    # # csv_headers = [ "GPUIndex", "GPUName", "GPUUtlizationPercent", "GPUMemoryUsagePercent", "GPUMemoryTotal", "GPUMemoryUsed", "PowerUsage"]
    # out = k8api.pod_exec(podname, ctnr, namespace, command, v1)
    out_data = {}

    for podname in podnames:
        print("connecting to pod " + podname[0])
        # Approach using python subprocesses & kubectl (must have a valid kubectl installation locally)
        powershell_command = "kubectl exec "+ podname[0] +" -n "+ NAMESPACE +" -c "+ SIMULATION_CONTAINER +" -- nvidia-smi --query-gpu=index,name,utilization.gpu,utilization.memory,memory.total,memory.used,power.draw --format=csv,noheader"
        out = subprocess.run(powershell_command, capture_output=True, shell=True, text=True)        
        #print(out.stdout)
        data = out.stdout
        data = data[:-1].split(',')

        if len(data) != 7:
            print("Error getting gpu_data, backing off & trying again...")
            time.sleep(5)
            data = record_gpu((podname, podname))

        out_data[podname[1]] = data

    return out_data

# signal_pod() --> helper fxn to singal each pod to report metrics
    # The logging library is called remotely via exec in each running pod.
    # This could be changed so that the running pods signal once a test case is reached
    # Once a pod is signaled it sends its data to the server before terminating.
# arg pod: name of pod to be signaled
# arg max_attempts: defaults to 4, maximum attempts to contact a pod
def signal_pod(pod, max_attempts=4):

    # dynamically grab container?
    powershell_command = "kubectl exec "+ pod +" -n "+ NAMESPACE +" -c "+ API_CONTAINER +" -- python -c \"import AutoDRIVE_API.logger as logger;logger.send_metrics()\""
    attempts = 0

    while attempts < max_attempts:
        try:
            result = subprocess.run(powershell_command, capture_output=True, text=True, shell=True, check=True)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempts + 1} failed with error: {e}")
            attempts += 1
            time.sleep(1)  # Add a delay between attempts

    print(f"Max attempts reached. Command '{powershell_command}' could not be executed successfully.")
    return None

    
# get_server_database() --> wrapper function to query and download the server's current database of metrics.
def get_server_database():
    response = requests.get(SERVER_IP+'collectdata')
    data = response.json()

    # print(data)
    return data

# reset_server_database() --> wrapper function to query and reset the server's database.
#   This is done before collection to assure no repeat entries.
def reset_server_database():
    response = requests.post(SERVER_IP+'resetdatabase')
    print(response.json())

# collect_pod_metrics() --> Function to tell each pod to send metrics to server using signal_pod(), 
#   then download the metrics from the server with get_server_database().
# arg pods: list of running pods
def collect_pod_metrics(pods):

    # Reset server database to get rid of old entries
    reset_server_database()

    # exec into each pod & run the send_metrics command from the logging library
    for pod in pods:
        if DEPLOYMENT in pod:
            signal_pod(pod)
            time.sleep(1) # wait 1 second to not spam the server & cause errors
    
    # Then connect to the server endpoint & download the files/array of data.
    data = get_server_database()
    return data


# process_simulation_data() --> Function to process server database from simulations.
#       Data is received in a 3d array, database[pod][entry][metric], processed, and saved to a labled csv
# arg data_3d: server database dump
# arg output_file: name of csv file
def process_simulation_data(data_3d, output_file="aeb_metrics.csv"):
    if not data_3d:
        print("No data provided.")
        return

    try:
        for layer_num, data in enumerate(data_3d, start=1):
            if not data:
                print(f"Skipping empty data in layer {layer_num}.")
                continue

            # Extract headers from the first row
            headers = data[0]

            # Extract data excluding the header
            rows = data[1:]

            # If it's the first layer, open the file in write mode, otherwise, open in append mode
            mode = 'w' if layer_num == 1 else 'a'

            with open(output_file, mode, newline='') as csvfile:
                # Create a CSV writer
                csv_writer = csv.writer(csvfile)

                # Write the header only for the first layer
                if layer_num == 1:
                    csv_writer.writerow(headers)

                # Write the data rows
                csv_writer.writerows(rows)

            print(f"CSV data for layer {layer_num} appended to {output_file} successfully.")

    except Exception as e:
        print(f"Error appending CSV data: {e}")

# watch_simulation() --> function to coordinate collecting resource data during simulation & time properly
#       every time interval record resource metrics of cluster.
# arg batch_number: batch number identifier used for csv name
# arg pods: list of running simulation pods
# arg recording_interval: seconds between recording resources, defaults to 5
# arg timer_duration: total time for simulation batch (seconds)
def watch_simulation(batch_number, pods, recording_interval=5, timer_duration=5*60):

    # record every recording_interval seconds
    cur_time = 0

    while cur_time < timer_duration:

        record_resource_metrics("hpc_metrics_" + str(batch_number) + ".csv", pods)
        time.sleep(recording_interval)
        cur_time = cur_time + recording_interval

    print("Timer completed.")

# launch_simulations() --> function to launch simulation pods & block until they are running
# arg max_attempts: number of attempts to connect to the cluster, defaults to 4
# arg num_pods: number of total simulation pods to be launched, defaults to be 16
def launch_simulations(max_attempts=4, num_pods=16):
    attempts = 0
    # Scale up to 16 & block
    powershell_command = "kubectl -n "+NAMESPACE+" scale deployment "+DEPLOYMENT+" --replicas=" + str(num_pods)

    while attempts < max_attempts:
        try:
            result = subprocess.run(powershell_command, capture_output=True, text=True, shell=True, check=True)
            print(result)
            break
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempts + 1} failed with error: {e}")
            attempts += 1
            time.sleep(1)  # Add a delay between attempts (optional)

    while(k8api.check_pending_pods()):
        print("waiting 5 sec for deployment...")
        time.sleep(5)
    # Simulations launched

# terminate_simulations() --> function to tear down simulation pods & block until everything is terminated
#     calls function from the kubernetes api wrapper
# arg max_attempts: max attempts to contact the cluster, defaults to 4
def terminate_simulations(max_attempts=4):
    # scale down to zero, pods to launch, begin collecting metrics

    powershell_command = "kubectl -n "+NAMESPACE+" scale deployment "+DEPLOYMENT+" --replicas=0"
    attempts = 0

    while attempts < max_attempts:
        try:
            result = subprocess.run(powershell_command, capture_output=True, text=True, shell=True, check=True)
            print(result)
            break
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempts + 1} failed with error: {e}")
            attempts += 1
            time.sleep(1)  # Add a delay between attempts (optional)

    while(k8api.check_terminating_pods()):
        print("waiting 5 sec for termination...")
        time.sleep(5)

# iterate_simulator_conditions() --> function to tell the server to move to the next batch of simulation configurations
#   wrapper for the control server endpoint
def iterate_simulator_conditions():
    response = requests.post(SERVER_IP+'iterate_simulation_conditions')
    print(response.json())

