# Makefile for docker/kubectl processes

SHELL := /bin/bash
.PHONY: build

# Command to generate the authentication file for the gitlab registry
# Be sure to fill out your own username & server
auth: rcd-reg-cred.yaml
rcd-reg-cred.yaml:
	@printf  "Password: " && \
		read -s pass && \
		docker login -u access-token -p "$$pass" SERVER_IP && \
		kubectl -n autodrive-simulator create secret docker-registry rcd-reg-cred \
			--docker-server="SERVER_IP" \
			--docker-username="USERNAME" \
			--docker-password="$$pass" \
			--dry-run="client" \
			-o yaml > rcd-reg-cred.yaml
build-backend:
# Build & Push the node backend
	cd ./node_server && docker build --platform=linux/amd64 -f node.Dockerfile -t registry.rcd.clemson.edu/viprgs_v_n_v/hpc_cloud_solutions/nodebackend:latest . && \
		docker push registry.rcd.clemson.edu/viprgs_v_n_v/hpc_cloud_solutions/nodebackend:latest && \
		kubectl -n autodrive-simulator delete pod $$(kubectl -n autodrive-simulator get pods -l=app=webapp -o jsonpath="{.items[*].metadata.name}")

build-frontend:
# Build & Push the webviewer
	docker build --platform=linux/amd64 -f webviewer.Dockerfile -t registry.rcd.clemson.edu/viprgs_v_n_v/hpc_cloud_solutions/webviewer:latest . && \
		docker push registry.rcd.clemson.edu/viprgs_v_n_v/hpc_cloud_solutions/webviewer:latest && \
		kubectl -n autodrive-simulator delete pod $$(kubectl -n autodrive-simulator get pods -l=app=webapp -o jsonpath="{.items[*].metadata.name}")

build-autodrive:
# Build & Push AutoDRIVE container
	docker build --platform=linux/amd64 -f autodrive_vulkan.Dockerfile -t registry.rcd.clemson.edu/viprgs_v_n_v/hpc_cloud_solutions/autodrive-1:latest . && \
		docker push registry.rcd.clemson.edu/viprgs_v_n_v/hpc_cloud_solutions/autodrive-1:latest    

build-autodrive-api:
# Build & Push AutoDRIVE Python API container
	docker build --platform=linux/amd64 -f autodriveAPI.Dockerfile -t registry.rcd.clemson.edu/viprgs_v_n_v/hpc_cloud_solutions/autodrive-api:latest . && \
		docker push registry.rcd.clemson.edu/viprgs_v_n_v/hpc_cloud_solutions/autodrive-api:latest 