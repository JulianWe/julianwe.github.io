FROM ubuntu:bionic
WORKDIR ansible/roles/webpage/files  
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nginx
RUN apt-get install vim -y
RUN apt-get install npm -y
RUN apt-get install nodejs -y

RUN pwd
RUN ls

COPY . /var/www/html/
COPY nginx.conf /etc/nginx/sites-enabled/default

CMD ["nginx", "-g", "daemon off;"]
