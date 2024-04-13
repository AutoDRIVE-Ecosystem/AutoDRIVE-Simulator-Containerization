# AutoDRIVE Simulator Containerization - Palmetto Tests

This branch contains various AutoDRIVE Simulator tests, which focus on AEB algorithm testing for OpenCAV.

They are meant to be run on Palmetto - Clemson's High-Performance Computing cluster. 

Each test is stored in its own sub-folder, under _palmetto/_. In order to reproduce any one of these tests, you need to upload the corresponding sub-folder to your Palmetto home folder, update the relevant paths within each script, and then submit the corresponding job script via Palmetto's QSUB scheduler:

    qsub autodrive_test.sh

It is assumed that you have an installation of the proper version of AutoDRIVE Simulator. Please refer to the instructions below to setup a containerized installation of AutoDRIVE Simulator, by use of a sandboxed singularity container. 

All tests also rely on the **autodrive** conda environment being available to you on Palmetto. This environment can be recreated, as needed, from the file _palmetto/environment.yml_, using the following command 

    conda env create -n autodrive -f environment.yml

## Containerized AutoDRIVE Simulator Installation on Palmetto 

In order perform the installation, you first need to procure a docker image for the correct version of AutoDRIVE Simulator. This image can be built using the instructions provided in this same repository, under the **docker** branch.

After having uploaded this image to dockerhub, you may build a singularity sandbox for it under your Palmetto home folder, as follows 

    cd ~
    singularity build --sandbox autodrive_simulator/ docker://<user>/<image_name>

