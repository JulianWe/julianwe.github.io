# How To Convert Markdown to file to HTML and build a Dockercontainer 

**How to convert README.md file to HTML with utf-8 encoding**
```sh
iconv -t utf-8 README.md | pandoc -t html -o README.html | iconv -f utf-8
``` 

**How to build docker container**
```yml
FROM ubuntu:bionic

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nginx
RUN apt-get install npm -y
RUN apt-get install nodejs -y

COPY ./app /var/www/html/

CMD ["nginx", "-g", "daemon off;"]
``` 

**How to run docker container**
```sh
docker build -t akash-webapp .

docker run -d -p 8080:80 akash-webapp

docker images -a

docker login --username victorynox0815

docker tag webapp victorynox0815/myrepo:webapp

docker push victorynox0815/myrepo:webapp
``` 
