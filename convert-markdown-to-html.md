# How To Convert Markdown to file to HTML and build a Dockercontainer 


**How to convert README.md file to HTML with utf-8 encoding**
```sh
iconv -t utf-8 README.md | pandoc -t html -o README.html | iconv -f utf-8
``` 



**How to build & run docker container**
```sh
docker build -t akash-webapp .

docker run -d -p 8080:80 akash-webapp
``` 
