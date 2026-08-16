import os
import requests
import json
import urllib.parse
import random
from datetime import datetime
from bs4 import BeautifulSoup

API_KEY = "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"
URL = "https://openrouter.ai/api/v1/chat/completions"

# Array of topics to keep generated titles dynamic & unique every day
TOPICS = [
    "Autonomous AI Agents in Modern Web Development",
    "Automated Web Scraping and Lead Extraction Pipelines",
    "Building High-Performance Next.js and Vercel Apps",
    "AI-Driven Code Optimization and Automated Workflows",
    "The Future of Web Development and AI Automation in 2026",
    "Full-Stack Python Automation and API Integration Guide"
]

def generate_article():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        'HTTP-Referer': 'https://codewithzaid.vercel.app/',
        'X-Title': 'CodeWithZaid'
    }
    
    selected_topic = random.choice(TOPICS)
    
    prompt_text = (
        f"Write a unique, highly professional blog post about '{selected_topic}'. "
        "Provide the output strictly as clean HTML using an <h1> for the article title, followed by <h2> subheadings and <p> content paragraphs. "
        "Do not write raw code block markers, markdown ticks, or html backticks."
    )
    
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",
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
            content = res_json['choices'][0]['message']['content']
            content = content.replace("```html", "").replace("```", "").strip()
            return content, selected_topic
        except (KeyError, IndexError):
            return "<p>Error parsing response content.</p>", selected_topic
    else:
        return f"<p>API Error: {response.text}</p>", selected_topic

def update_blog_listing(today, title):
    blog_page_path = "blog.html"
    if not os.path.exists(blog_page_path):
        return

    with open(blog_page_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    blog_grid = soup.find("div", class_="card-grid") or soup.find("div", class_="blog-grid")
    if blog_grid:
        existing_card = blog_grid.find("a", href=f"blog/{today}.html")
        if not existing_card:
            new_card = soup.new_tag("article", **{"class": "card"})
            
            encoded_title = urllib.parse.quote(title)
            random_seed = random.randint(1, 9999)
            dynamic_img_url = f"https://image.pollinations.ai/prompt/{encoded_title}?width=600&height=350&nologo=true&seed={random_seed}"
            
            card_content = f"""
              <div class="card-img-wrapper">
                <img src="{dynamic_img_url}" alt="{title}">
              </div>
              <div class="card-topic-box">
                <span class="topic-title">AI & Tech</span>
              </div>
              <div class="card-body">
                <h3>{title}</h3>
                <p>A fresh, hands-on exploration into modern developer workflows and automation.</p>
                <div class="card-action">
                  <a href="blog/{today}.html" class="read-btn">Read More →</a>
                </div>
              </div>
            """
            new_card.append(BeautifulSoup(card_content, "html.parser"))
            blog_grid.insert(0, new_card)

            with open(blog_page_path, "w", encoding="utf-8") as f:
                f.write(str(soup))

def save_html_file(content, topic_title):
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("blog", exist_ok=True)
    filename = f"blog/{today}.html"

    # Extract dynamic h1 title if generated inside AI content
    extracted_title = topic_title
    if "<h1>" in content and "</h1>" in content:
        try:
            extracted_title = content.split("<h1>")[1].split("</h1>")[0]
        except IndexingError:
            pass

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{extracted_title} — CodeWithZaid</title>
    <link rel="stylesheet" href="../style.css">
    <script defer src="/_vercel/insights/script.js"></script>
    <style>
        /* Smooth vertical scrolling and reading layout for laptop/desktop */
        html, body {{
            overflow-x: hidden;
            overflow-y: auto !important;
            height: auto !important;
            min-height: 100vh;
        }}
        .blog-post-article {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px 80px;
            line-height: 1.8;
        }}
        .blog-post-article h1 {{
            font-size: 2.2rem;
            margin-bottom: 24px;
            background: linear-gradient(90deg, #ffffff 0%, #00f0ff 50%, #ffffff 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}
        .blog-post-article h2 {{
            font-size: 1.5rem;
            margin-top: 32px;
            margin-bottom: 16px;
            color: var(--accent-2, #00f0ff);
        }}
        .blog-post-article p {{
            font-size: 1.05rem;
            margin-bottom: 20px;
            color: var(--text-muted, #c3c7d5);
        }}
    </style>
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
    
    <main class="wrap page-header">
        <article class="blog-post-article">
            {content}
        </article>
    </main>

    <footer class="site-footer">
      <div class="wrap footer-inner">
        <span class="footer-copy">&copy; 2026 CodeWithZaid.online</span>
      </div>
    </footer>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    update_blog_listing(today, extracted_title)

if __name__ == "__main__":
    article_html, topic = generate_article()
    save_html_file(article_html, topic)
