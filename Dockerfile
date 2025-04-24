FROM ubuntu:bionic

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nginx
RUN apt-get install vim -y
RUN apt-get install npm -y
RUN apt-get install nodejs -y

COPY ansible/roles/ /var/www/html/
COPY ansible/roles/webpage/files/ /var/www/html/
COPY ansible/roles/webpage/files/nginx.conf /etc/nginx/sites-enabled/default

CMD ["nginx", "-g", "daemon off;"]
