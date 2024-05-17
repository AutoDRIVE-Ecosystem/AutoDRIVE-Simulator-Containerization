# AutoDRIVE Simulator HPC

This repository contains HPC deployments of the AutoDRIVE Simulator.

This project utlizes the Kubernetes API to enable dynamic, scalable, and disposable AutoDRIVE simulations on an HPC cluster. The basic structure of a project's deployment is displayed in the graphic below. Each simulation pod contains a AutoDRIVE simulation container and an AutoDRIVE Devkit container integrated with the python HPC Framework Data Logging Module. Simulation batches are scripted with the python HPC Framework Automation Module to allow for dynamic simulation cases across HPC resources. Simulation data is collected from a control server pod located inside the kubernetes cluster & exports data to a thin client. Additionally live simulations can be monitored from the AutoDRIVE Simulation Webviewer. 

![Workflow Diagram](/Media/hpc_system_overview.png)

## SETUP

**Pre-requisites**: Kubectl, Docker, Python 3.8+, python packages listed in requirements.txt, download desired versions
of AutoDRIVE simulator & AutoDRIVE devkit, configure Kubectl with access to desired cluster.
<!-- todo: add setup steps
- install k8
- install docker 
- install python & necessary packages
 - requirement.txt
- Download AutoDRIVE Devkit & Simulator
- Pull Dockerfiles -->

### Rancher/Gitlab Container Instructions

These steps outline how to properly build and run docker images hosted on a gitlab container registry, as well as how to properly configure a rancher cluster to pull from a project's container registry. These steps assume docker & kubectl are already installed on a user's machine.


1. Download the KubeConfig from the top righthand corner of the Rancher dashboard & apply it to your kubectl by pointing the environment variable ``` KUBECONFIG ``` to the downloaded configuation file's location. Be sure to test your connectivity to the cluster with a basic kubectl commands such as ``` kubectl get pods ```.

![KubeConfig Download](/Media/kubeconfig_download.png)
<br>

2. An authentication token is needed in order to access the Gitlab container registry for the project. Use the ``` auth ``` command inside ```/Docker/Makefile``` to generate an authentication file for the container registry, insert your token in as the requested password. This will also generate a ``` rcd-reg-cred.yaml ``` which can be applied to the cluster to give kubernetes access to the Gitlab registry. Be sure to update the appropriate Username & Server IP in the Makefile command.
<br>

3. To build a docker image that is going to be hosted in the container registry tag it using the structure ``` <server_url>/<gitlab_group>/<project_name>/<container_name> ```.
<br>

4. After building the docker image with the proper naming structure & authenticating with docker, you should be able to push the built image to the container registry with ``` docker push <tag> ```. The pushed container should appear in the selected gitlab project's registry found by selecting **Deploy --> Container Registry**. You may need your project owner to enable this feature. ```/Docker/Makefile``` has examples of commands to deploy the containers used in this project. 

![Container Registry](/Media/container_registry.png)
<br>

5. You should now be able to run docker images hosted in the container registry on the cluster & use them in your deployments.

## USAGE

If using Clemson University's Rancher cluster, ```example_script.py``` is a script which provides a baseline use case.

## FILE STRUCTURE

**Docker/**: The ```Docker``` directory contains all necessary files to compile docker images containing the AutoDRIVE
Simulator, AutoDRIVE Devkit, simulation webviewer, and the backend control server. A Makefile contains necessary commands
to compile each docker image. The dockerfiles expect ```AutoDRIVE_API``` and ```AutoDRIVE_Simulator``` directories to be
placed here (populated with simulator & devkit files). 

It should be noted the ```logger.py``` file may need to be moved into a new AutoDRIVE_API folder & integrated into the
AutoDRVIE vehicle script in order to enable data collection from pods inside the cluster.

**Kubernetes/**: The ```Kubernetes``` directory contains the yaml files for deployments used in the cluster. 

**Python/**: The ```Python``` directory holds all of the scripts to control simulations running in the cluster, namely
```automation_module.py```. Most variables can be updated using the ```config.ini``` file. 

## KNOWN ISSUES

1. The control server can sometimes crash if simulation conditions are not configured to have multiple conditions to iterate
through. This can generally be fixed by restarting the pod or adding duplicate conditions based on the desired number of
iterations. A current goal of this project is to re-implement the way simulation configurations are handled to not be
generated by the control server/inside the cluster.

2. Sometimes queries to the kubernetes api inside the cluster can result in network errors (both if called via python
subprocess + kubetl or via the python kubernetes client). There is a large amount of timeouts/repeat attempts built into
the automation library, but it can still be an issue for large workloads querying the same node in a cluster multiple 
times.

## CITATION

#### [Off-Road Autonomy Validation Using Scalable Digital Twin Simulations Within High-Performance Computing Clusters](https://arxiv.org/abs/2405.04743)
```bibtex
@eprint{AutoDRIVE-HPC-RZR-2024,
title={Off-Road Autonomy Validation Using Scalable Digital Twin Simulations Within High-Performance Computing Clusters}, 
author={Tanmay Vilas Samak and Chinmay Vilas Samak and Joey Binz and Jonathon Smereka and Mark Brudnak and David Gorsich and Feng Luo and Venkat Krovi},
year={2024},
eprint={2405.04743},
archivePrefix={arXiv},
primaryClass={cs.RO}
}
```
This work has been accepted at **2024 Ground Vehicle Systems Engineering and Technology Symposium (GVSETS). Distribution Statement A. Approved for public release; distribution is unlimited. OPSEC #8451.**
