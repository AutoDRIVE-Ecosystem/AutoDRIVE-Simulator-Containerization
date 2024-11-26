# AutoDRIVE Simulator: Rancher Cluster Deployments

This branch hosts resources for deployments of the AutoDRIVE Simulator on Rancher HPC cluster.

This project utlizes the Kubernetes API to enable dynamic, scalable, and disposable AutoDRIVE simulations on an HPC cluster. The basic structure of a project's deployment is displayed in the graphic below. Each simulation pod contains an `AutoDRIVE Simulator` container and an `AutoDRIVE Devkit` container integrated with the `Python HPC Framework Data Logging Module`. Simulation batches are scripted with the `Python HPC Framework Automation Module` to allow for dynamic simulation cases across HPC resources. Simulation data is collected from a control server pod located inside the Kubernetes cluster, which exports data to a thin client. Additionally, live simulations can be monitored from the `AutoDRIVE HPC Webviewer`.

![Workflow Diagram](/Media/hpc_system_overview.png)

## SETUP

**Prerequisites**:
- `kubectl`
- `Docker`
- `Python 3.8+`
- Python packages listed in [`requirements.txt`](Docker/requirements.txt)
- Desired versions of `AutoDRIVE Simulator` & `AutoDRIVE Devkit`
- Configure `kubectl` with access to the desired cluster
<!-- TODO: add setup steps
- install k8
- install docker 
- install python & necessary packages
- requirement.txt
- Download AutoDRIVE Devkit & Simulator
- Pull Dockerfiles -->

### Rancher/Gitlab Container Instructions

These steps outline how to properly build and run Docker images hosted on a GitLab container registry, as well as how to properly configure a Rancher cluster to pull from a project's container registry. These steps assume `Docker` & `kubectl` are already installed on a user's machine.

1. Download the `KubeConfig` from the top right-hand corner of the Rancher dashboard & apply it to your `kubectl` by pointing the environment variable `KUBECONFIG` to the downloaded configuration file's location. Be sure to test your connectivity to the cluster with a basic `kubectl` command such as `kubectl get pods`.

![KubeConfig Download](/Media/kubeconfig_download.png)
<br>

2. An authentication token is needed in order to access the GitLab container registry for the project. Use the `auth` command inside [`/Docker/Makefile`](Docker/Makefile) to generate an authentication file for the container registry, and insert your token in as the requested password. This will also generate an `rcd-reg-cred.yaml` file, which can be applied to the cluster to give Kubernetes access to the GitLab registry. Be sure to update the appropriate `Username` & `Server IP` in the Makefile command.
<br>

3. To build a Docker image that is going to be hosted in the container registry tag it using the structure `<server_url>/<gitlab_group>/<project_name>/<container_name>`.
<br>

4. After building the Docker image with the proper naming structure & authenticating with Docker, you should be able to push the built image to the container registry with `docker push <tag>`. The pushed container should appear in the selected GitLab project's registry found by selecting **Deploy &#8594; Container Registry**. You may need your project owner to enable this feature. [`/Docker/Makefile`](Docker/Makefile) has examples of commands to deploy the containers used in this project. 

![Container Registry](/Media/container_registry.png)
<br>

5. You should now be able to run docker images hosted in the container registry on the cluster & use them in your deployments.

## USAGE

If using Clemson University's Rancher cluster, [`example_script.py`](Python/example_script.py) is a script that provides a baseline use case.

## FILE STRUCTURE

- **[Docker](Docker)**: The `Docker` directory contains all necessary files to compile Docker images containing the AutoDRIVE
Simulator, AutoDRIVE Devkit, AutoDRIVE HPC Webviewer, and the backend control server. A Makefile contains the necessary commands
to compile each Docker image. The Dockerfiles expect the `AutoDRIVE_API` and `AutoDRIVE_Simulator` directories to be placed here
(populated with Simulator & Devkit files). It should be noted the [`logger.py`](Docker/AutoDRIVE_API/logger.py) file may need to
be moved into a new `AutoDRIVE_API` folder & integrated into the [AutoDRIVE DevKit](Docker/AutoDRIVE_API/rzr_aeb.py) script in
order to enable data collection from pods inside the cluster.

- **[Kubernetes](Kubernetes)**: The `Kubernetes` directory contains the `YAML` files for deployments used in the cluster. 

- **[Python](Python)**: The `Python` directory holds all the necessary scripts to control simulations running in the cluster, using
[`automation_module.py`](Python/automation_module.py). Most variables can be updated using the [`config.ini`](Python/config.ini) file. 

## KNOWN ISSUES

1. The control server can sometimes crash if simulation conditions are not configured to have multiple conditions to iterate
through. This can generally be fixed by restarting the pod or adding duplicate conditions based on the desired number of
iterations. A future goal of this project is to re-implement the way simulation configurations are handled to not be
generated by the control server inside the cluster.

2. Sometimes queries to the Kubernetes API inside the cluster can result in network errors (both if called via Python
subprocess + `kubetl` or via the Python Kubernetes client). There are a large number of timeouts/repeat attempts built into
the automation library, but it can still be an issue for large workloads querying the same node in a cluster multiple 
times.

## CITATION

#### [Off-Road Autonomy Validation Using Scalable Digital Twin Simulations Within High-Performance Computing Clusters](https://arxiv.org/abs/2405.04743)
```bibtex
@inproceedings{DT-HPC-VnV-2024,
title={Off-Road Autonomy Validation Using Scalable Digital Twin Simulations Within High-Performance Computing Clusters},
author={{Samak, Tanmay} and {Samak, Chinmay} and {Krovi, Venkat} and {Binz, Joey} and {Luo, Feng} and {Smereka, Jonathon} and {Brudnak, Mark} and {Gorsich, David}},
booktitle={2024 NDIA Michigan Chapter Ground Vehicle Systems Engineering and Technology Symposium},
publisher={National Defense Industrial Association},
month={sep},
year={2024},
doi={https://doi.org/10.4271/2024-01-4111},
url={https://doi.org/10.4271/2024-01-4111}
}
```
This work has been accepted at **2024 Ground Vehicle Systems Engineering and Technology Symposium (GVSETS).** The publication can be found on [GVSETS Library](https://ndia-mich.org/images/events/gvsets/2024/papers/MSPV/320PMO~1.PDF), and is archived on [SAE Mobilus](https://doi.org/10.4271/2024-01-4111).
