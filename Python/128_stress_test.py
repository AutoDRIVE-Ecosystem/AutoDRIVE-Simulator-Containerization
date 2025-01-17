import automation_module

if __name__ == '__main__':

    #
    #   128, 64, 32, 16, 8, 4, 2, 1
    #

    total_batches = 8
    batch_num = 0
    batch_size= 1
    simulation_length = 60*5

    ##############################################
    #
    # EXAMPLE SIMULATION LOOP 
    #
    ##############################################

    # Tear down any currently running simulations
    print("Cleaning up any currently running simulations...")
    automation_module.terminate_simulations()

    print("Starting batch load of size " + str(total_batches) + "...")
    # For each batch
    while( batch_num < total_batches ):
        print("BEGINNING BATCH " + str(batch_num) + " ------------------------------")
        # launch simulations
        print("Launching simulations...")
        automation_module.launch_simulations(num_pods=batch_size)

        # Get pods to pass along
        v1 = automation_module.k8api.init_k8api()
        out = automation_module.k8api.get_pods_with_nodes(v1)
        pods_with_nodes = out[0]
        pods = out[1]

        # watch & collect resource data
        print("Simulations launched, collecting & saving resource data to " + "hpc_metrics_"+str(batch_num)+".csv" + "...")
        automation_module.watch_simulation(batch_num, pods_with_nodes, timer_duration=simulation_length)

        # collect & simulation data
        print("Simulations finished, collecting simulation data from pods & server database...")
        sim_data = automation_module.collect_pod_metrics(pods)

        # process simulation data & save locally
        print("Simulation data collected, saving to aeb_metrics_" + str(batch_num) + ".csv...")
        automation_module.process_simulation_data(sim_data, output_file=("aeb_metrics_"+str(batch_num)+".csv"))

        # tear down old simulations
        print("Simulation data processed, terminating simulations...")
        automation_module.terminate_simulations()

        print("BATCH " + str(batch_num) + " COMPLETED ------------------------------")

        batch_num = batch_num + 1
        batch_size = batch_size * 2

