# AutoDRIVE Simulator: Docker Containerization

This branch provides the necessary resources to build and run a Docker image for [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator).

> [!NOTE]
> - It is assumed that [Docker](https://docs.docker.com/engine/install) is installed.
> - It is assumed that if the Docker container is to take advantage of an NVIDIA GPU, the host machine has been properly configured by installing the necessary NVIDIA GPU drivers and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html).

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

## Running the AutoDRIVE Simulator Docker Image

To run the built Docker image for AutoDRIVE Simulator, execute:
```bash
xhost local:root
docker run --rm -it --network=host --ipc=host -v /tmp/.X11-unix:/tmp.X11-umix:rw --env DISPLAY --privileged --gpus all autodrive_simulator
```

## Generally Helpful Docker Tips
1. To access the container while it is running, execute the following command in a new terminal window to start a new bash session inside the container:
```bash
docker exec -it <container_name> bash
```

2. To exit the bash session(s), simply execute:
```bash
exit
```

3. To kill the container, execute the following command:
```bash
docker kill <container_name>
```

4. To remove the container, simply execute:
```bash
docker rm <container_name>
```

5. Running or caching multiple docker images, containers, volumes, and networks can quickly consume a lot of disk space. Hence, it is always a good idea to frequently check docker disk utilization:
```bash
docker system df
```

6. To avoid utilizing a lot of disk space, it is a good idea to frequently purge docker resources such as images, containers, volumes, and networks that are unused or dangling (i.e. not tagged or associated with a container). There are several ways with many options to achieve this, please refer to appropriate documentation. The easiest way (but a potentially dangerous one) is to use a single command to clean up all the docker resources (dangling or otherwise):
```bash
docker system prune -a
```
