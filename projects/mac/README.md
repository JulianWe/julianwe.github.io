https://hub.docker.com/r/sickcodes/docker-osx 
https://github.com/sickcodes/Docker-OSX
https://hub.docker.com/r/sickcodes/docker-osx

sudo chmod 666 /var/run/docker.sock

docker run -it --device /dev/kvm -p 50922:10022 -v /tmp/.X11-unix:/tmp/.X11-unix -e "DISPLAY=${DISPLAY:-:0.0}" sickcodes/docker-osx:latest
