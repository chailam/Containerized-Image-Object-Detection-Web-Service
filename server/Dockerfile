### Dockerfile
# docker build -t iweblens .
# docker image build -t cloi0001/iweblens:1.0.0 .    if push to dockerhub


# set the base image
FROM python:3.9-slim-buster

# create working directory to  instructs Docker to use this path as the default location for all subsequent commands. 
# by doing this, we do not have to type out full file paths but can use relative paths based on the working directory.
WORKDIR /server

# inform Docker that the container listens on the specified network ports at runtime. 
# this does not actually publish the port but functions as a type of documentation
# docker run -d -p 5000:5000 <imageName>, the reason to map is because the container is containerized while running. 
# to communicate with the hosted VM while running as container, it has to specify port, such that <port of VM>:<port of container>
EXPOSE 5000

# set the environment for flask 
# host 0.0.0.0 means listen on all public IPs
# flask app specify the app.py to run
ENV FLASK_APP iWebLens_server.py
ENV FLASK_RUN_HOST 0.0.0.0

# add label
LABEL author="Chai Lam Loi"

# copy all files in local machine to container
COPY . .

# upgrade pip version
RUN pip install --upgrade pip
RUN apt-get update

# the required dependencies for opencv
RUN apt-get install ffmpeg libsm6 libxext6  -y

# install all dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# run the script
CMD ["flask", "run"]
