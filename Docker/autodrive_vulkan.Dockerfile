####################################################
#
#   AutoDRIVE Simulator Dockerfile
#
####################################################

FROM nvidia/vulkan:1.1.121-cuda-10.1--ubuntu18.04
ENV DEBIAN_FRONTEND=noninteractive
ENV XDG_RUNTIME_DIR=/tmp/runtime-dir
ARG VERSION

# Add CUDA repository key and install packages
RUN apt-key adv --fetch-keys "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub" \
    && apt update \
    && apt install -y --no-install-recommends \
        nano \
        vim \
        sudo \
        curl \
        unzip \
        libvulkan1 \
        libc++1 \
        libc++abi1 \
        vulkan-utils \
    && rm -rf /var/lib/apt/lists/*

# Install tools for display
RUN apt update --fix-missing \
    && apt install -y x11vnc xvfb xtightvncviewer ffmpeg

# Install Python
RUN apt update && apt install -y python3

# Copy over AutoDRIVE files
COPY AutoDRIVE_Simulator /home/AutoDRIVE_Simulator
COPY entrypoint.sh home/AutoDRIVE_Simulator
COPY httpserver.py home/AutoDRIVE_Simulator

# Set work directory and register executable
WORKDIR /home/AutoDRIVE_Simulator
RUN chmod +x /home/AutoDRIVE_Simulator/AutoDRIVE\ Simulator.x86_64
