# Prism Syntax highlighting



https://github.com/PrismJS/prism-themes/tree/master/template

https://prismjs.com/#examples


``inline code formatting``


```bash
cd ~

brew untap ovrclk/tap
brew tap akash-network/tap
brew install akash-provider-services

brew install jq -y
brew install unzip -y
brew install coreutils -y 

curl -sfL https://raw.githubusercontent.com/akash-network/node/master/install.sh | bash
curl -s "$AKASH_NET/genesis.json" > genesis.json 
curl -s "$AKASH_NET/seed-nodes.txt" | paste -d, -s
curl -s "$AKASH_NET/peer-nodes.txt" | paste -d, -s

sudo mv ./bin/akash /usr/local/bin
sudo mv ./bin/provider-services /usr/local/bin
```


```yaml
- name: build html website
  hosts: localhost
  connection: localhost
  gather_facts: False
  vars:
    path: "/Users/jw/Documents/GitHub/julianwe.github.io"

  tasks:
    - name: convert README to HTML
      shell: | 
        cd {{ path }}
        for folder in projects/*; do pandoc -f markdown $folder/README.md > projects/${folder#*/}/${folder#*/}.html;  
        done
        ls {{ path }}/projects
      register: folder

    - name: set project, URLs & directorys facts
      set_fact:
        name: "{{ item | trim ('/')}}"
        file_path: "{{ path }}/projects/{{ item }}/{{ item | trim ('/')}}.html"
        jinja2_file_path:  "{{ path }}/projects/ansible/projects_html.j2"
        url: "https://julianwe.github.io/projects/{{ item }}/{{ item | trim('/')}}.html"
        identifier: "{{ index }}"
      loop: "{{ folder.stdout_lines }}"
      loop_control:
        index_var: index
      register: facts

    - name: set html content facts
      set_fact:
        html: "{{ lookup('file', item.ansible_facts.file_path) }}"
        file_path: "{{ item.ansible_facts.file_path }}"
        url: "{{ item.ansible_facts.url }}"
        identifier: "{{ item.ansible_facts.identifier }}"
        name: "{{ item.ansible_facts.name }}"
      loop: "{{ facts.results }}"
      register: html_files

    - name: create project HTML sites
      template:
        src: "{{ jinja2_file_path }}"
        dest: "{{ item.ansible_facts.file_path }}"
      delegate_to: localhost
      when: item.ansible_facts.name != "template"
      loop: "{{ html_files.results }}"

    - name: Deploy Website on IPFS
      command: ipfs add -r {{ path }}
```




