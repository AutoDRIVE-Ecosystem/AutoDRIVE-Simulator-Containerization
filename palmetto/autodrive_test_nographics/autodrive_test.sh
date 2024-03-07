#!/bin/bash

#PBS -N autodrive_test
#PBS -l select=1:ngpus=2:ncpus=16:mpiprocs=16:mem=120gb:interconnect=hdr,walltime=0:02:00
#PBS -J 1-16
#PBS -m abe
#PBS -M giovanm@clemson.edu
#PBS -j oe

export TEST_DIR=/home/giovanm/autodrive_test_nographics/
export SIMULATOR_DIR=/home/giovanm/autodrive_simulator_autoconnect_weather_time/
export XDG_RUNTIME_DIR=/tmp/runtime-dir

# Activate the autodrive conda environment
module add anaconda3/2022.05-gcc/9.5.0
source activate autodrive

# Run test instance
$TEST_DIR/run_test_instance.sh
