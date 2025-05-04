FROM ubuntu:bionic

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nginx
RUN apt-get install vim -y
RUN apt-get install npm -y
RUN apt-get install nodejs -y

COPY . /var/www/html/
COPY nginx.conf /etc/nginx/sites-available/

CMD ["nginx", "-g", "daemon off;"]
