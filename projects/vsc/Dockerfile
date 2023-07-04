FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nginx
RUN apt-get install npm -y
RUN apt-get install nodejs -y
RUN apt-get install vim -y
RUN apt-get install -q -y ssmtp mailutils
RUN apt-get install software-properties-common -y

COPY . /var/www/html/

CMD ["nginx", "-g", "daemon off;"]

