from os import path
from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException
import time
import configparser

#############################################################
#
#   KUBERNETES PYTHON CLIENT WRAPPER MODULE
#
#############################################################

# This module wraps parts of the kubernetes python client & exposes functionality
    # used in other modules of the hpc python framework

# Edit to your config file path, if using the Rancher cluster you can download this from the website
# PATH_TO_CONFIG="C:\\Users\\joeyd\Desktop\\Research2022\\vnv\\viprgs-test.yaml"
# PATH_TO_CONFIG="/home/jbinz/viprgs-test.yaml"
# Kubernetes project namespace

# Configure Parameters
configp = configparser.ConfigParser()

# Read the .ini file
configp.read('config.ini')

# Extract values
NAMESPACE = configp['DEFAULT']['namespace']
PATH_TO_CONFIG = configp['DEFAULT']['path_to_config']

VERBOSE = False

# K8API FUNCTION DEFINITIONS

# function to initialize the API with default cluster info
# returns client v1, make sure you have properly configured PATH_TO_CONFIG
def init_k8api():
    config.load_kube_config(config_file=PATH_TO_CONFIG)
    v1 = client.CoreV1Api()

    return v1

# log_resources() --> kubectl top nodes
def log_resources():
    api = client.CustomObjectsApi()
    k8s_nodes = api.list_namespaced_custom_object("v1", "node", NAMESPACE, "nodes")
    print(k8s_nodes)


# pod_exec() --> executes command in a selected pod
# arg name: pod name
# arg ctnr: container name
# arg namespace: pod namespace 
# arg command: command to be executed
# arg v1: k8s client
# Reference: https://martinheinz.dev/blog/73
def pod_exec(name, ctnr, namespace, command, v1):
    exec_command = ["/bin/sh", "-c", command]

    response = stream(v1.connect_get_namespaced_pod_exec,
                      name,
                      namespace,
                      command=exec_command,
                      container=ctnr,
                      stderr=True, stdin=False,
                      stdout=True, tty=False,
                      _preload_content=False)
    
    while response.is_open():
        response.update(timeout=1)
        if response.peek_stdout():
            out = response.read_stdout()
            if(VERBOSE): print(f"STDOUT: \n{out}")
        if response.peek_stderr():
            if(VERBOSE): print(f"STDERR: \n{response.read_stderr()}")

    response.close()

    if response.returncode != 0:
        raise Exception("Script failed")
    else:
        return out

# get_pods() --> Helper fxn returns a list of every pod name in the given namespace
# arg v1: k8s client
# return pods: list of pod names from namespace NAMESPACE
def get_pods(v1):
    MAX_RETRIES = 4
    RETRY_DELAY = 5

    for attempt in range(MAX_RETRIES):
        try:
            if VERBOSE:
                print("getting pods in the {} namespace".format(NAMESPACE))
            ret = v1.list_namespaced_pod(namespace=NAMESPACE, watch=False)
            pods = [i.metadata.name for i in ret.items]
            return pods
        except Exception as e:
            print("Error getting pods: {}".format(e))
            if attempt < MAX_RETRIES - 1:
                print("Retrying in {} seconds...".format(RETRY_DELAY))
                time.sleep(RETRY_DELAY)
            else:
                print("Max retries reached. Exiting.")
                raise

def get_pods_with_nodes(v1):
    MAX_RETRIES = 4
    RETRY_DELAY = 5

    for attempt in range(MAX_RETRIES):
        try:
            if VERBOSE:
                print("Getting pods in the {} namespace".format(NAMESPACE))
            ret = v1.list_namespaced_pod(namespace=NAMESPACE, watch=False)
            pod_info = [(pod.metadata.name, pod.spec.node_name) for pod in ret.items]
            pods = [i.metadata.name for i in ret.items]
            return (pod_info, pods)
        except Exception as e:
            print("Error getting pods: {}".format(e))
            if attempt < MAX_RETRIES - 1:
                print("Retrying in {} seconds...".format(RETRY_DELAY))
                time.sleep(RETRY_DELAY)
            else:
                print("Max retries reached. Exiting.")
                raise

# delete_all_pods() --> Deletes all pods to be reset
# !!! use carefully, can break things !!!
# arg v1: k8s client
def delete_all_pods(v1):
    print("resetting carla pods...")
    pods = get_pods(v1)
    if len(pods) <= 8:
        for pod in pods:
            if "carla-pod" in pod:
                v1.delete_namespaced_pod(pod, NAMESPACE)
                print("deleted pod " + pod + " ...")
    else:
        print("error too many pods must fully re-deploy.")

# check_terminating_pods() --> Used to wait for all pods to terminate
# arg namespace: namespace of pods to check
# arg max_attempts: max amount of attempts if a network error is encountered
# return bool: true if pods are still terminating, false if no pods are shutting down
def check_terminating_pods(namespace=NAMESPACE, max_attempts=3):
    attempts=0
    while attempts < max_attempts:
        try:
            # Create a Kubernetes API client
            config.load_kube_config(config_file=PATH_TO_CONFIG)
            api_instance = client.CoreV1Api()
            
            # Get the list of pods in the specified namespace
            pods = api_instance.list_namespaced_pod(namespace)

            if (len(pods.items) == 1) and ('webviewer' in pods.items[0].metadata.name):
                return False # return false if no pods still shutting down (webviewer is the only pod)
            else:
                return True # return true if other pods are still running

        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}")
            attempts += 1
            time.sleep(1)

    print("Max attempts reached, failed to check terminating pods.")
    return False

# check_pending_pods() --> Used to wait for all pods to start up
# arg namespace: namespace of pods to check
# arg max_attempts: max amount of attempts if a network error is encountered
# return bool: true if pods are still launching, false if all pods have successfully launched
def check_pending_pods(namespace=NAMESPACE, max_attempts=3):
    attempts=0
    while attempts < max_attempts:
        try:
            # Load Kubernetes configuration from default location
            config.load_kube_config(config_file=PATH_TO_CONFIG)

            # Create a Kubernetes API client
            api_instance = client.CoreV1Api()

            # Get the list of pods in the specified namespace
            pods = api_instance.list_namespaced_pod(namespace)

            # Check if any pod is in the "Terminating" phase
            pending_pods = [pod.metadata.name for pod in pods.items if pod.status.phase != 'Running']

            if pending_pods:
                return True # return true if any pods still launching
            else:
                return False # return false if all pods are running

        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}")
            attempts += 1
            time.sleep(1)

    print("Unable to check pending pods, max attempts reached.")
    return False