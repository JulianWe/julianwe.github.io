# How to setup the grapth curator on any server

**Install npm & nvm**
```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")" [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" 
nvm install 20.18.1
nvm use 20.18.1
```

**Install the Graph CLI**
```sh
# On your local machine, run one of the following command
npm install -g @graphprotocol/graph-cli@latest
```

**Initialize your Subgraph**
```sh
# The following command initializes your Subgraph from an existing contract and indexes events:
graph init
```

