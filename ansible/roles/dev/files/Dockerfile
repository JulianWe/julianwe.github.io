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