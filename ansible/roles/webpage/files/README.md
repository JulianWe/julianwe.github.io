# ⚙️ Deploy Website using Ansible, Docker and GitHub Pages

![](../images/ansible-docker.jpg)


```text
This Blogpost describes how to deploy your own webpage with ansible roles, docker and GitHub pages 
using readme files from github and coverts each readme file into a HTML Blogpost. 
This allows you to automate all blogposts using ansible roles. ⚙️
``` 

```sh
This Blogpost describes how to deploy your own webpage with ansible roles, docker and GitHub pages using Markdown files from github and coverts each README file into a HTML Blogpost. This allows you to automate all blogposts using ansible roles. ⚙️
``` 

**before we can start make sure to install ansible and docker.**
```sh 
brew update
brew upgrade
brew cleanup

brew install ansible
brew install --cask docker
```

**create a new repository with your username.github.io.**
```sh
git init username.github.io
git clone https://github.com/JulianWe/julianwe.github.io.git
cp julianwe.github.io/* username.github.io/
``` 

**run ansible playbook webpage.yml to build your own webpage with your own blog like this on github.**
```sh
# run ansible playbook with your information and build your own website NOTE: customize ansible/roles/webpage/vars/main.yml file with your information before you proceed.

export ANSIBLE_CONFIG=/Users/jw/Documents/GitHub/julianwe.github.io/ansible/ansible.cfg
cd julianwe.gituhub.io/ansible
ansible-playbook playbooks/webpage.yml
```

**build your own website with ansible role playbook "webpage.yml".**
```sh
---
- hosts: localhost 
  tasks:

    - name: Include variables from a file
      include_vars:
        file: "../roles/webpage/vars/main.yml"
      register: vars
      
    - name: Include the webpage role
      include_role:
        name: roles/webpage 
...
```


**the playbook webpage.yml starts two playbooks to build our webpage with a local webserver before we are able to deploy our website on github pages.**
```yml
# tasks file for webpage

  - name: "Include playbook webpage"
    import_tasks: playbook_webpage.yml

  - name: "Include playbook webserver"
    import_tasks: playbook_webserver.yml

```

**the playbook_webpage.yml convert reamdme files into html blogposts and creates our index.html file using ansible and our jinja 2 template**
```yml
---
- name: convert README files to HTML
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
    url: "https://julianwe.github.io/{{ item }}/{{ item | trim('/')}}.html"
  loop: "{{ folder.stdout_lines }}"
  loop_control:
    index_var: index
  register: facts

  # this task sets our html content for every blogpost as fact 
- name: set html content facts
  set_fact:
    html: "{{ lookup('file', item.ansible_facts.file_path) }}"
    file_path: "{{ item.ansible_facts.file_path }}"
    url: "{{ item.ansible_facts.url }}"
    name: "{{ item.ansible_facts.name }}"
  loop: "{{ facts.results }}"
  register: html_files

  # In this Task we loop over our convertet readme files and use ansible template module to build one html blogpost per readme.
- name: create project HTML sites
  template:
    src: "{{ blogpost }}"
    dest: "{{ item.ansible_facts.file_path }}"
  delegate_to: localhost
  loop: "{{ html_files.results }}"

  # This task builds our index.html file with our blog section using jinjja 2 templates like described in the next step.
- name: build index html file
  template:
    src: "{{ index_html }}"
    dest: "{{ index_file }}"
  delegate_to: localhost
...
``` 


**This jinja 2 template ansible/roles/webpage/templates/blogpost.j2 is used to build our blog section and index.html file with the information provided inside our ansible/roles/webpage/vars/main.yml blogpost section and our other sections.**
```html
    <section class="blog section " id="blog">
        <div class="container">
            <div class="row">
                <div class="section-title padd-15">
                    <h2>Blog Posts</h2>
                </div>
            </div>

            <!-- Projects Section -->
            <div class="w3-container w3-padding-32" id="Projects">

                <!-- partial:index.partial.html -->
                <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet">
                <link rel="stylesheet" href="css/cards.css">
                <section class="hero-section">
                    <div class="card-grid">

                        {% for blogpost in vars.blogposts  %}
                            <a class="card" href={{ blogposts[blogpost].html }}> 
                                <div class="card__background"
                                    style="background-image: url({{ blogposts[blogpost].image }})"></div>
                                <div class="card__content">
                                    <p class="card__category">{{ blogposts[blogpost].category }}</p>
                                    <h3 class="card__heading">{{ blogposts[blogpost].description }}</h3>
                                </div>
                            </a>
                        {% endfor %}

                    <div>
                </section>
            </div>
        </div>
    </section>
```


**this html jinja2 template is used for our converte readme files and builds one html blogpost for every readme file.**
```html
<!DOCTYPE html>
<html lang="en">

<head>
  <title>{{ vars.home.title }}</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon"
    href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='48' height='48' viewBox='0 0 16 16'><text x='0' y='14'>🐇</text></svg>" />
  <link rel="stylesheet" href={{ vars.paths.blog_css }}>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
</head>

<body class="dark">
    <div class="main-container">
        <div class="aside">
            <div class="logo">
                <a href="../index.html#home"><span></span>{{ vars.home.title }}</a>
            </div>

            <div class="nav-toggler">
                <span></span>
            </div>

            <ul class="nav">
                <li><a href="../index.html#home"><i class="fa fa-home"></i>Home</a></li>
                <li><a href="../index.html#about"><i class="fa fa-user"></i>About</a></li>
                <li><a href="../index.html#services"><i class="fa fa-list"></i>Services</a></li>
                <li><a href="../index.html#blog" class="active"><i class="fa fa-briefcase"></i>Blog</a></li>
                <li><a href="../index.html#contact"><i class="fa fa-comments"></i>Contact</a></li>
                <li><a href="https://github.com/JulianWe/julianwe.github.io"><i class="fa-brands fa-github"></i>GitHub</a></li>
            </ul>
        </div>
    </div>

  <section class="blogpost section " id="blogpost">
      <div class="container">

          <link rel="stylesheet" href="{{ vars.paths.markdown_css }}">
          <link rel="stylesheet" href="{{ vars.paths.md_css }}">
          
          <!-- Start README.md -->

          {{ item.ansible_facts.html }}

          <!-- End README.md -->
      </div>
  </section>

  <!-- JavaScript -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/typed.js/2.0.10/typed.min.js"></script>
  <script src={{ vars.paths.script_js }}></script>
  <script src={{ vars.paths.prism_js }}></script>

</html>
``` 

**the playbook ansible/roles/webpage/tasks/playbook_webserver.yml starts a local webserver for testing purpose using ansible and docker.**
```yml
---
- name: stop all running docker containers
  shell:
    cmd: docker stop $(docker ps -a -q)

- name: build docker container
  shell:
    cmd: docker build -t webpage "{{ vars.paths.repository }}"

- name: run docker container
  shell:
    cmd: docker run -d -p 8080:80 webpage

- name: open webpage 
  shell:
    cmd: open http://localhost:8080 
...
``` 


**make sure that your dockerfile for github pages resides in our username.github.io repository**
```dockerfile
FROM ubuntu:bionic

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nginx
RUN apt-get install vim -y
RUN apt-get install npm -y
RUN apt-get install nodejs -y

COPY ansible/roles/webpage/files /var/www/html/
COPY nginx.conf /etc/nginx/sites-enabled/default

CMD ["nginx", "-g", "daemon off;"]

```

**make sure to select deploy from branch instead of GitHub Actions in [repository settings](https://github.com/username/username.github.io/settings/pages) this enables github pages for your repository and deploys your webpage with github action on every push**
![](../images/pages.jpg)


