# AutoDRIVE Simulator: Docker Containerization

This repository provides the necessary resources to build and run a Docker image for [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator).

> Note It is assumed that if the Docker container is to take advantage of an NVIDIA GPU, the host machine has been properly configured by installing the necessary NVIDIA GPU drivers, [Docker](https://docs.docker.com/engine/install), and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html).

## Building the AutoDRIVE Simulator Docker Image

To build a Docker image for the latest AutoDRIVE Simulator release version, execute:
```bash
docker build -t autodrive_simulator .
```

To use a specific release version instead, use the `VERSION` build argument and execute:
```bash
docker build -t autodrive_simulator . --build-arg VERSION=Simulator-0.2.0
```

For testing purposes, you may want to use a local version of the AutoDRIVE Simulator executable, as opposed to pulling a release version from GitHub. In such a case, update the [Dockerfile](Dockerfile) with the folder name containing your AutoDRIVE Simulator standalone executable, and execute:
```bash
docker build -t autodrive_simulator . --build-arg VERSION=local
```
