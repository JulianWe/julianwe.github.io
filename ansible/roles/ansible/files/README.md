# Build HTML files using Ansible

![](../../ansible/files/images/ansible-1.jpg)

**requirements**
```sh 
brew install ansible
```

**Convert Singel README file using Pandoc CLI**
```sh 
pandoc -f markdown -t html5 README.md > test.html
```

**Convert README files to HTML using bash script**
```sh 
#!/bin/bash
cd /Users/jw/Documents/GitHub/julianwe.github.io
for folder in projects/*/; do echo ${folder#*/};  done
for folder in projects/*; do pandoc -f markdown $folder/README.md > test/${folder#*/}.html;  done
```

**Or convert README files to HTML using Ansible Playbook**
```yml
---
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
...
```

**Jinja2 HTML Project Template & Variables**

| Name | Description | Example values |
| --- | --- | --- |
|`html`| README to HTML content without j2 | `{{ item.ansible_facts.html }}` |
|`url`| Website URL. | `"{{ item.ansible_facts.url }}"` |
|`identifier`| disqus comment page identifier. | `{{ item.ansible_facts.identifier }}` |
|`name`| Browser Title | `{{ item.ansible_facts.name }}` |

```html
<html>

<head>
  <meta charset="UTF-8">
  <!-- Browser Titel CHANGE-->
  <title>{{ item.ansible_facts.name }}</title>
  <!-- Favicon  -->
  <link rel="icon" href="https://akash-web-prod.s3.amazonaws.com/uploads/2020/02/cropped-akash-logo-192x192.png"
    sizes="192x192" />
  <!-- CSS  -->
  <link rel="stylesheet" href="../../css/splendor.css">
  <script src="https://code.jquery.com/jquery-3.7.0.js"></script>
</head>

<!-- Navbar -->
<div class="topnav">
  <div class="w3-bar w3-white w3-wide w3-padding w3-card">
    <!-- Float links to the right. Hide them on small screens -->
    <p class="right">
      <a href="../../index.html" class="w3-bar-item w3-button"><b>GitBlog</a>
      <a href="../../projects.html" class="w3-bar-item w3-button">Projects</a>
      <a href="../../about.html" class="w3-bar-item w3-button">About</a>
      <a href="../../contact.html" class="w3-bar-item w3-button">Contact</a>
      <a href="../../search.html" class="w3-bar-item w3-button">🔍</a>
  </div>
</div>

<!-- Start README -->

{{ item.ansible_facts.html }}

<!-- END README -->

<!-- Hide show comments -->
<p class="w3-right"><button class="w3-button w3-white" onclick="hideClick('show_disqus_thread')"><b>Comments
      &nbsp;</b>💬</span></button></p>

<link rel="stylesheet" href="../../css/w3.css">
<p class="w3-clear"></p>

<div id="show_disqus_thread" style="display:none">

  <!-- Comments -->
  <div id="disqus_thread"></div>
  <script>
    /**
    *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM  https://disqus.com/admin/universalcode/#configuration-variables    */
    var disqus_config = function () {
      this.page.url = "{{ item.ansible_facts.url }}"; 
      this.page.identifier = {{ item.ansible_facts.identifier }}; 
      identifier variable
    };

    (function () { // DON'T EDIT BELOW THIS LINE
      var d = document, s = d.createElement('script');
      s.src = 'https://https-julianwe-github-io-1.disqus.com/embed.js';
      s.setAttribute('data-timestamp', +new Date());
      (d.head || d.body).appendChild(s);
    })();
  </script>
  <script id="dsq-count-scr" src="//https-julianwe-github-io-1.disqus.com/count.js" async></script>
  <div class="blog-post-comments">
    <div id="disqus_thread">
      <noscript>Please enable JavaScript to view the comments.</noscript>
    </div>
  </div>
</div>

<!-- Functions -->
<script>
  function hideClick() {
    var x = document.getElementById("show_disqus_thread");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }
  function menu() {
    var x = document.getElementById("links");
    if (x.style.display === "block") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
  }
</script>

</body>
</html>
```


**Run Ansible Playbook**
```sh 
ansible-playbook /Users/jw/Documents/GitHub/julianwe.github.io/projects/ansible/playbook.yml -vvv
```



