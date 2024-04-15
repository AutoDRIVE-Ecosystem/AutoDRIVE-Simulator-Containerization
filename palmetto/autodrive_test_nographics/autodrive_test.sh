#!/bin/bash

#PBS -N autodrive_test
#PBS -l select=1:ngpus=2:ncpus=16:mpiprocs=16:mem=120gb:interconnect=hdr,walltime=0:02:00
#PBS -J 1-16
#PBS -m abe
#PBS -M giovanm@clemson.edu
#PBS -j oe

export TEST_DIR=/home/giovanm/autodrive_test_nographics/
export SIMULATOR_DIR=/home/giovanm/autodrive_autoconnect/
export XDG_RUNTIME_DIR=/tmp/runtime-dir

# Record job performance metrics
jobperf -record -w -rate 5s -record-db $TEST_DIR/autodrive_test_perf.db > /dev/null 2>&1 &

# Activate the autodrive conda environment
module add anaconda3/2022.05-gcc/9.5.0
source activate autodrive

# Run test instance
$TEST_DIR/run_test_instance.sh
