# AutoDRIVE Simulator: Docker Containerization

This repository provides the necessary files to build a docker image for AutoDRIVE Simulator. 

It is assumed that if the docker container is to take advantage of an NVIDIA GPU, the host machine has been properly configured by installing the necessary NVIDIA drivers, [Docker](https://docs.docker.com/engine/install/), and the  
[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html). 

## Building an AutoDRIVE Simulator Docker Image

In order to build a docker image for AutoDRIVE Simulator, run

`docker build -t autodrive_simulator .`

This will automatically pull the latest AutoDRIVE Simulator release version. To use a specific release version instead, use the VERSION command line argument. For instance, you may run

`docker build -t autodrive_simulator . --build-arg VERSION=Simulator-0.2.0`

For testing purposes, you may want to use a local version of AutoDRIVE Simulator, as opposed to pulling a release version from github. In this case, 
update the Dockerfile with the folder name containing your AutoDRIVE Simulator application, and run 

`docker build -t autodrive_simulator . --build-arg VERSION=local`
