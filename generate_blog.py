import os
from google import generativeai as genai
from datetime import datetime

API_KEY = "AizzaSyB0KzFytUr9GkEm8uEbHkEglnak"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
prompt = (
    "Write a 100% unique, highly engaging, human-like, and completely original blog post about 'The Future of Web Development and AI Automation in 2026'. "
    "Ensure the content is completely plagiarism-free, creative, and written from a professional developer's perspective. "
    "Format the output cleanly in clean HTML (use <h2>, <p>, <ul>, <li> tags inside a main article structure) "
    "So it can be directly published on a website. Do not include markdown code block ticks like ```html in the output, just raw HTML body content."
)

response = model.generate_content(prompt)
html_content = response.text

def save_html_file(content):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"blog/{today}.html"

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
    <main>
        <article>
            {content}
        </article>
    </main>
    <footer>
        <p>&copy; 2026 CodeWithZaid. All rights reserved.</p>
    </footer>
</body>
</html>
"""

    os.makedirs("blog", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    article_html = generate_article()
    save_html_file(article_html)
