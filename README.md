# iWebLens Project 
** Image Object Detection Web Service within a Containerised Environment**

## Project Summary

The iWebLens project aims to develop a web-based system that enables users to submit images to a Docker container-hosted web service and receive a list of objects detected in their uploaded image. 

The system utilizes the YOLO (You Only Look Once) library, a cutting-edge real-time object detection system, and the OpenCV (Open-Source Computer Vision Library) for necessary image operations. Both YOLO and OpenCV are Python-based open-source libraries for computer vision and machine learning. The web service is containerized within a Docker container and deployed in a Kubernetes cluster, serving as the orchestration system. The object detection web service is implemented as a RESTful API, leveraging Python's Flask library. 

The project focuses on evaluating the performance of iWebLens by varying the request rate (demand) and the number of Pods in the Kubernetes cluster (resources).

## Project Components

1. **Web Service**
   - Develop a RESTful API using Flask to handle image uploads in JSON object format.
   - Utilize YOLO and OpenCV for object detection.
   - Ensure multi-threading support for concurrent client requests.

2. **Dockerfile**
   - Create a Dockerfile to build a Docker image for the object detection web service.
   - Include necessary instructions for dependencies and configuration.

3. **Kubernetes Cluster**
   - Deploy a Kubernetes cluster on a virtual machine in the Nectar cloud using Kind.
   - Configure the cluster with a single controller and worker node.
   - Follow Kind's quick start guide for setting up the cluster.

4. **Kubernetes Service**
   - Create service and deployment configurations for the object detection pods.
   - Set CPU request and limit to "0.5" for each pod.
   - Expose the deployment to communicate with the web service from external sources using Nodeport.

5. **Experiments**
   - Conduct experiments to evaluate the impact of varying client thread count and pod count on response time.
   - Run experiments with different combinations of thread counts (1, 6, 11, 16, 21, 26, 31) and pod counts (1, 2, 3).
   - Plot the results in a 2-D line plot and analyze trends.



## Installation
The basic Python packages are part of the Python installation. You also need to install Python packages, including Flask, opencv-python and numpy. Make sure you use Python 3.5 or higher and upgrade your pip tool. 

If any Linux dependencies are required, you shall install them based on system requirements.



## Instruction to Run
1. Create a Docker image for the web server using Dockerfile in `server` folder. 
2. Use Kind to build a cluster
3. Apply the Kubernetes deployment YAML file to the cluster.
4. Apply the service YAML file to cluster
5. Send the client request using `iWebLens_client.py` file.
6. Test the performance under difference pod numbers and thread using `autoCollect.py` file.

You can refer to the `Sample Docker_K8S Command.txt` for some Docket / Kubernetes command.
