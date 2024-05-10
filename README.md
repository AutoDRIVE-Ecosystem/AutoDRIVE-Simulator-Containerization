# AutoDRIVE Simulator: RZR AEB Function

<p align="center">
<img src="https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-Simulator-HPC/blob/rzr-aeb/media/rzr-aeb-scenario.gif"/>
</p>

This branch hosts the necessary codebase to run a parameter sweep for verification and validation (V&V) of autonomous emergency braking (AEB) functionality of the [RZR digital twin](https://youtu.be/PLW1-sYW6Hw) using [AutoDRIVE Simulator](https://youtu.be/t0CgNR_LgrQ).

This branch, in conjunction with others such as the [palmetto](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-Simulator-HPC/tree/palmetto) and [palmetto-webviewer](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-Simulator-HPC/tree/palmetto-webviewer) or the [rancher](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-Simulator-HPC/tree/rancher) and [rancher-webviewer](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-Simulator-HPC/tree/rancher-webviewer), can deploy the said V&V framework on the respective high-performance cloud computing resources.

## SETUP

1. Clone `rzr-aeb` branch of the `AutoDRIVE-Simulator-HPC` repository.
    ```bash
    $ git clone --single-branch --branch rzr-aeb https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-Simulator-HPC.git
    ```
2. Give executable permissions to all the Python scripts.
   ```bash
   $ cd <path/to/cloned/repo>
   $ sudo chmod +x *.py
   ```
4. Install the necessary dependencies as mentioned below.
    [AutoDRIVE Devkit's Python API](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit/ADSS%20Toolkit/autodrive_py) has the following dependencies (tested with Python 3.8.10):
    
    - Websocket-related dependencies for communication bridge between [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator) and [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) (version sensitive):
    
      | Package | Tested Version |
      |---------|----------------|
      | eventlet | 0.33.3 |
      | Flask | 1.1.1 |
      | Flask-SocketIO | 4.1.0 |
      | python-socketio | 4.2.0 |
      | python-engineio | 3.13.0 |
      | greenlet | 1.0.0 |
      | gevent | 21.1.2 |
      | gevent-websocket | 0.10.1 |
      | Jinja2 | 3.0.3 |
      | itsdangerous | 2.0.1 |
      | werkzeug | 2.0.3 |
      
      ```bash
      $ pip3 install eventlet==0.33.3
      $ pip3 install Flask==1.1.1
      $ pip3 install Flask-SocketIO==4.1.0
      $ pip3 install python-socketio==4.2.0
      $ pip3 install python-engineio==3.13.0
      $ pip3 install greenlet==1.0.0
      $ pip3 install gevent==21.1.2
      $ pip3 install gevent-websocket==0.10.1
      $ pip3 install Jinja2==3.0.3
      $ pip3 install itsdangerous==2.0.1
      $ pip3 install werkzeug==2.0.3
      ```
    
    - Generic dependencies for data processing and visualization (usually any version will do the job):
    
      | Package | Tested Version |
      |---------|----------------|
      | numpy | 1.13.3 |
      | pillow | 5.1.0 |
      | opencv-contrib-python | 4.5.1.48 |
      
      ```bash
      $ pip3 install numpy
      $ pip3 install pillow
      $ pip3 install opencv-contrib-python
      ```

## USAGE

1. Download, unzip and launch the AutoDRIVE Simulator by referring to the detailed instructions given [here](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE/tree/AutoDRIVE-Simulator?tab=readme-ov-file#download-and-run):
   - Download the latest release of the standalone application of AutoDRIVE Simulator for RZR AEB scenario from [here](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-Simulator-HPC/releases/download/rzr-aeb-0.1.0/AutoDRIVE.Simulator.zip).
   - Set the execution rights of the standalone application:
     ```bash
     $ cd <path/to/AutoDRIVE Simulator.x86_64>
     $ sudo chmod +x AutoDRIVE\ Simulator.x86_64
     ```
   - Run the standalone simulator by double-clicking the standalone executable or via command line interface (CLI):
     ```bash
     $ cd <path/to/AutoDRIVE Simulator.x86_64>
     $ ./ AutoDRIVE\ Simulator.x86_64
     ```

2. Execute the [`rzr_aeb`](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-Simulator-HPC/blob/rzr-aeb/rzr_aeb.py) Python3 script to run the autonomous emergency braking (AEB) function with RZR, employing the AutoDRIVE Python API.
    ```bash
    $ cd <path/to/rzr_aeb.py>
    $ python3 rzr_aeb.py
    ```

    <p align="center">
    <img src="https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-Simulator-HPC/blob/rzr-aeb/media/rzr-aeb-demo.gif"/>
    </p>

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
