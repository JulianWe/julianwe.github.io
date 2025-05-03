FROM ubuntu:latest

WORKDIR /root
COPY ./privkey.json /root
RUN apt-get update && apt-get upgrade
RUN apt-get install curl -y
RUN curl -LO https://github.com/AIOZNetwork/aioz-dcdn-cli-node/files/13561206/aioznode-darwin-amd64-1.1.0.tar.gz
RUN tar xzf aioznode-darwin-amd64-1.1.0.tar.gz
RUN mv aioznode-darwin-amd64-1.1.0 aioznode
RUN chmod +x /root/aioznode
RUN export PATH=$PATH:/root/aioznode
RUN aioznode start --home nodedata --priv-key-file privkey.jsons