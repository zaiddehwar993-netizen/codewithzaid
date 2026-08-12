import os
import datetime
from google import generativeai as genai

API_KEY = "AIzaSyB0bTzkFYf0g6FnmMURLEgob8khEwginak"
genai.configure(api_key=API_KEY)

def generate_article():
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        "Write a 100% unique, highly engaging, human-like, and completely original blog post about 'The Future of Web Development and AI Automation in 2026'. "
        "Ensure the content is completely plagiarism-free, creative, and written from a professional developer's perspective. "
        "Format the output cleanly in clean HTML (use <h2>, <p>, <ul>, <li> tags inside a main article structure) "
        "so it can be directly published on a website. Do not include markdown code block ticks like ```html in the output, just raw HTML body content."
    )
    response = model.generate_content(prompt)
    return response.text

def save_html_file(content):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"blog-{today}.html"
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unique AI Blog - {today}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <a href="index.html">Home</a>
            <a href="blog.html">Blog</a>
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
        </nav>
    </header>
    <main style="padding: 20px; max-width: 800px; margin: auto;">
        {content}
    </main>
    <footer>
        <p>&copy; 2026 CodeWithZaid. All rights reserved.</p>
    </footer>
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    article_html = generate_article()
    save_html_file(article_html)
  
