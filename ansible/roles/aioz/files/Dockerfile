FROM ubuntu:latest

WORKDIR /root
RUN apt update && apt upgrade -y
RUN apt install curl -y
COPY privkey.json /root
RUN curl -LO https://github.com/AIOZNetwork/aioz-dcdn-cli-node/files/13561211/aioznode-linux-amd64-1.1.0.tar.gz
RUN tar xzf aioznode-linux-amd64-1.1.0.tar.gz
RUN mv aioznode-linux-amd64-1.1.0 /root/aioznode
COPY privkey.json /root
RUN /root/aioznode start --home nodedata --priv-key-file /root/privkey.json