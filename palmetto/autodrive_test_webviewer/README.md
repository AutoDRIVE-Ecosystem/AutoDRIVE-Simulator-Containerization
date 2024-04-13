# Palmetto WebViewer Test

In order to run this test, on top of submitting the test script to the QSUB scheduler, as usual, with the command 

    qsub autodrive_test.sh

we have a separate step to deploy the webviewer. 

This is done by executing - for instance, from an interactive job - the script _deploy_webviewer.sh_. Notice that the TARGET variable within the script may need to be updated to point to your specific AutoDRIVE Simulator installation.

To access the WebViewer from outside the Palmetto cluster using a local browser, you first need to set up a 
SOCKS v5 tunnelling connection from your local machine, as explained in the [Palmetto Docs](https://docs.rcd.clemson.edu/palmetto/connect/proxy/).
