import os
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

# OpenRouter API Configuration
API_KEY = "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"
URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_article():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        'HTTP-Referer': 'https://codewithzaid.vercel.app/',
        'X-Title': 'CodeWithZaid'
    }
    
    prompt_text = (
        "Write a 100% unique, highly engaging, human-like, and completely original blog post about 'The Future of Web Development and AI Automation in 2026'. "
        "Ensure the content is completely plagiarism-free, creative, and written from a professional developer's perspective. "
        "Format the output cleanly in clean HTML (use <h2>, <p>, <ul>, <li> tags inside a main article structure) "
        "So it can be directly published on a website. Do not include markdown code block ticks like ```html in the output, just raw HTML body content."
    )
    
    payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": prompt_text
            }
        ]
    }
    
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        res_json = response.json()
        try:
            return res_json['choices'][0]['message']['content']
        except (KeyError, IndexError):
            return "<p>Error parsing response content.</p>"
    else:
        return f"<p>API Error: {response.text}</p>"

def update_blog_listing(today, title="The Future of Web Development and AI Automation"):
    blog_page_path = "blog.html"
    if not os.path.exists(blog_page_path):
        return

    with open(blog_page_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    blog_grid = soup.find("div", class_="blog-grid")
    if blog_grid:
        existing_card = blog_grid.find("a", href=f"blog/{today}.html")
        if not existing_card:
            new_card = soup.new_tag("article", **{"class": "card"})
            
            card_content = f"""
              <div class="card-image"><img src="[https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=500&q=60](https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=500&q=60)" alt="AI automation"></div>
              <div class="card-body">
                <span class="card-tag">AI Automation</span>
                <h3>{title}</h3>
                <p>A fresh, AI-generated exploration into modern development workflows and tools for 2026.</p>
                <a href="blog/{today}.html" class="card-link">Read More →</a>
              </div>
            """
            new_card.append(BeautifulSoup(card_content, "html.parser"))
            blog_grid.insert(0, new_card)

            with open(blog_page_path, "w", encoding="utf-8") as f:
                f.write(str(soup))

def save_html_file(content):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"blog/{today}.html"

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Future of Web Development and AI Automation in 2026 — CodeWithZaid</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header class="site-header">
      <nav class="nav wrap" aria-label="Primary">
        <a href="../index.html" class="logo"><span class="bracket">&lt;</span>CodeWithZaid<span class="bracket">/&gt;</span></a>
        <ul class="nav-links">
          <li><a href="../index.html">Home</a></li>
          <li><a href="../blog.html">Blog</a></li>
          <li><a href="../about.html">About</a></li>
          <li><a href="../contact.html">Contact</a></li>
        </ul>
      </nav>
    </header>
    <main class="wrap" style="padding: 40px 20px;">
        <article>
            {content}
        </article>
    </main>
    <footer class="site-footer">
      <div class="wrap footer-inner">
        <span class="footer-copy">&copy; 2026 CodeWithZaid. All rights reserved.</span>
      </div>
    </footer>
</body>
</html>
"""

    os.makedirs("blog", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    update_blog_listing(today)

if __name__ == "__main__":
    article_html = generate_article()
    save_html_file(article_html)
    
