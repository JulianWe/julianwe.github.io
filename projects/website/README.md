# How To Convert Markdown to file to HTML and build a Dockercontainer 

**How to convert README.md file to HTML with utf-8 encoding**

```sh
brew install pandoc

pandoc -f markdown README.md > index.html

or

iconv -t utf-8 README.md | pandoc -t html -o README.html | iconv -f utf-8
``` 


**How to build docker container**

```yml
FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nginx

RUN apt-get install npm -y
RUN apt-get install nodejs -y
RUN apt-get install vim -y

COPY . /var/www/html/

CMD ["nginx", "-g", "daemon off;"]
```


**How to run docker container**

```sh
#Dockerimage
docker build -t webapp .
docker images -a
docker run -d -p 8080:80 webapp

# DockerHub
docker login --username victorynox0815
docker tag webapp victorynox0815/myrepo:webapp
docker push victorynox0815/myrepo:webapp
``` 



**Combine Readme and Template**
```sh

#!/bin/bash

for folder in projects/*/; do echo ${folder#*/};  done

mkdir test

for folder in projects/*; do pandoc -f markdown $folder/README.md > test/${folder#*/}.html;  done
``` 


**Examplpe SDL File for Akash**

```yml
---
version: '2.0'
services:
  webapp:
    image: 'victorynox0815/docker-repo:webapp'
    expose:
      - port: 80
        as: 8080
        to:
          - global: true
profiles:
  compute:
    webapp:
      resources:
        cpu:
          units: 2
        memory:
          size: 512Mi
        storage:
          - size: 10Gi
  placement:
    dcloud:
      pricing:
        webapp:
          denom: uakt
          amount: 1000
deployment:
  webapp:
    dcloud:
      profile: webapp
      count: 1
``` 


