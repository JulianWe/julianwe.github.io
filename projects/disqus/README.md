# Implementing comments & recommendations 


**create disqus account https://disqus.com/**

*create a website shotname in my case*
https-julianwe-github-io-1


Replace the following URLs
‘https://https-julianwe-github-io-1.disqus.com/recommendations.js’
‘https://https-julianwe-github-io-1.disqus.com/embed.js’
‘https://https-julianwe-github-io-1.disqus.com/count.js’
url: https://julianwe.github.io/projects/akash/akash.html#disqus_thread
identifier: 1


```html
<!-- Recommendations -->
<div class="disqus_recommendations">
  <div id="disqus_recommendations"></div>
  <script>
    (function () {
      var d = document, s = d.createElement('script'); // IMPORTANT: Replace EXAMPLE with your forum shortname!
      s.src = 'https://https-julianwe-github-io-1.disqus.com/recommendations.js'; s.setAttribute('data-timestamp', +new Date()); // 
      (d.head || d.body).appendChild(s);
    })();
  </script>
  <noscript>
    Please enable JavaScript to view the
    <a href="https://disqus.com/?ref_noscript" rel="nofollow">
      comments powered by Disqus.
    </a>
  </noscript>
</div>
<!-- End Recommendations -->

<div class="disqus_thread">
  <!-- Comments -->
  <div id="disqus_thread"></div>
  <script>
    var disqus_config = function () {
      this.page.url = "https://julianwe.github.io/projects/akash/akash.html#disqus_thread";
      this.page.identifier = 3;
    };
    (function () { // DON'T EDIT BELOW THIS LINE
      var d = document, s = d.createElement('script');
      s.src = 'https://https-julianwe-github-io-1.disqus.com/embed.js';
      s.setAttribute('data-timestamp', +new Date());
      (d.head || d.body).appendChild(s);
    })();
  </script>
  <script id="dsq-count-scr" src='https://https-julianwe-github-io-1.disqus.com/count.js' async></script>
  <div class="blog-post-comments">
    <div id="disqus_thread">
      <noscript>Please enable JavaScript to view the comments.</noscript>
    </div>
  </div>
</div>
```

```css
div[class~="disqus_thread"] {
  #disqus_thread {
    position: relative;
    max-width: 36rem;
    margin-top: 1rem;
    margin-right: auto;
    margin-bottom: 1rem;
    margin-left: auto
  }

  #disqus_thread:after {

    content: "";
    display: block;
    height: 55px;
    width: 100%;
    position: absolute;
    bottom: 0;
    background: white;
  }
}

div[class~="disqus_recommendations"] {
  #disqus_recommendations:before {
    position: relative;
    max-width: 36rem;
    margin-top: 1rem;
    margin-right: auto;
    margin-bottom: 1rem;
    margin-left: auto
  }

  #disqus_recommendations:after {
    content: "";
    display: block;
    height: 55px;
    width: 100%;
    position: absolute;
    bottom: 0;
    background: white;
  }
}


```