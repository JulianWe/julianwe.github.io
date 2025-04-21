# Create a Website using Docker and GitHub Pages

![](../files/images/ansible-docker.jpg)

**create a new repository with your username.github.io**
```sh
git init julianwe.github.io
git clone https://github.com/JulianWe/julianwe.github.io.git
``` 

**How to build webserver with docker container**
```dockerfile
FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nginx

RUN apt-get install npm -y
RUN apt-get install nodejs -y
RUN apt-get install vim -y

COPY . /var/www/html/

CMD ["nginx", "-g", "daemon off;"]
```


**Build HTML Blog using ansible playbook**

```yml
---
- name: playbook_convert_makdown_html
  hosts: localhost
  connection: localhost
  gather_facts: False
  
  vars:
    path: "/Users/jw/Documents/GitHub/webpage/ansible"
    blogpost: "{{ path }}/roles/webpage/templates/blogpost.j2"
  
  tasks:

    - name: convert README to HTML
      shell: | 
        cd {{ path }}
        for folder in roles/*; do pandoc -f markdown -t html5 $folder/files/README.md > roles/${folder#*/}/files/${folder#*/}.html;  
        done;
        ls {{ path }}/roles
      register: folder

    - name: set project, URLs & directorys facts
      set_fact:
        name: "{{ item | trim ('/')}}"
        file_path: "{{ path }}/roles/{{ item }}/files/{{ item | trim ('/')}}.html"
        url: "https://julianwe.github.io/blogpost/{{ item }}/{{ item | trim('/')}}.html"
      loop: "{{ folder.stdout_lines }}"
      loop_control:
        index_var: index
      register: facts
  
    - name: set html content facts
      set_fact:
        html: "{{ lookup('file', item.ansible_facts.file_path) }}"
        file_path: "{{ item.ansible_facts.file_path }}"
        url: "{{ item.ansible_facts.url }}"
        name: "{{ item.ansible_facts.name }}"
      loop: "{{ facts.results }}"
      register: html_files

    - name: create project HTML sites
      template:
        src: "{{ blogpost }}"
        dest: "{{ item.ansible_facts.file_path }}"
      delegate_to: localhost
      loop: "{{ html_files.results }}"
...
``` 

![](../files/images/pages.jpg)


**Create .github/workflows/docker-image.yml Action file**

```yml
name: Docker Image CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:

  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Build the Docker image
      run: docker build . --file Dockerfile --tag my-image-name:$(date +%s)
``` 
