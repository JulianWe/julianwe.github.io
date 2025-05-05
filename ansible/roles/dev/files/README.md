# Cloud Development Container 


![](../images/docker.jpg)

```sh
# install github & clone this repository 
brew install git
git clone https://github.com/JulianWe/julianwe.github.io.git
cd julianwe.github.io/ansible/roles/dev/files
```


```dockerfile
# Create Dockerfile
FROM ubuntu:latest

WORKDIR /root

RUN apt-get update && apt-get upgrade
RUN apt-get install systemd -y 
RUN apt-get install apt-utils -y 
RUN apt-get install wsl -y 
RUN apt-get install git -y
RUN apt-get install curl -y 
RUN apt-get install vim -y
RUN apt-get install zsh -y
RUN apt-get install ansible -y
RUN apt-get install python3-pip -y
RUN apt-get install docker.io -y
RUN curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

COPY ./.vimrc /root/.vimrc
COPY ./.zshrc /root/.zshrc
```



```sh
# Build Docker Container inside the directory where the Dockerfile resides
docker build -t container .

# Run the container in detached interactive mode
docker run -d -it container

# Show running container
docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED        STATUS        PORTS      NAMES
a78f8f665291   container         "/bin/bash"              1 second ago   Up 1 second              affectionate_matsumoto

# Enter  docker container using container id 
docker exec -it a78f8f665291 /bin/bash

# tag docker image for docker hub
docker tag container victorynox0815/container:dev

# push docker image to docker hub
docker push victorynox0815/container:dev
```


