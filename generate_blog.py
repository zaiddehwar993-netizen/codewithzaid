import os
import requests
import json
import re
import random
import pathlib
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup

# SECURITY: API key is now read from an environment variable (GitHub Secret),
# never hardcoded in the file. Set OPENROUTER_API_KEY as a repo secret.
API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"

BASE_DIR = pathlib.Path(__file__).parent.resolve()
USED_TOPICS_FILE = BASE_DIR / "used_topics.json"

# ----------------------------------------------------------------------
# TOPIC POOL — each topic now has a proper cinematic image description
# so Pollinations generates a nice, professional thumbnail instead of a
# random/weird image from a bare title.
# ----------------------------------------------------------------------
TOPICS = [
    {"topic": "Autonomous AI Agents in Modern Web Development", "tag": "AI Agents",
     "img_prompt": "futuristic AI robot assistant coding on a holographic screen, neon blue cyberpunk office, cinematic 8k"},
    {"topic": "Automated Web Scraping and Lead Extraction Pipelines", "tag": "Web Scraping",
     "img_prompt": "digital data streams flowing into a futuristic server, glowing blue network visualization, cinematic render"},
    {"topic": "Building High-Performance Next.js and Vercel Apps", "tag": "Web Dev",
     "img_prompt": "sleek modern laptop displaying a glowing code editor, minimalist tech desk setup, cinematic lighting"},
    {"topic": "AI-Driven Code Optimization and Automated Workflows", "tag": "AI & Tech",
     "img_prompt": "abstract glowing circuit board with AI neural network pattern, futuristic blue and purple lighting, 8k render"},
    {"topic": "The Future of Web Development and AI Automation in 2026", "tag": "AI & Tech",
     "img_prompt": "futuristic city skyline with holographic web interfaces floating above, cyberpunk night scene, cinematic"},
    {"topic": "Full-Stack Python Automation and API Integration Guide", "tag": "Python",
     "img_prompt": "python code on a dual monitor setup, cozy dark tech workspace, warm ambient lighting, cinematic"},
    {"topic": "Mastering Prompt Engineering for Large Language Models", "tag": "AI & Tech",
     "img_prompt": "glowing brain made of digital text and code, futuristic AI concept art, cinematic blue lighting"},
    {"topic": "Serverless Architecture: Building Apps Without Managing Servers", "tag": "Cloud",
     "img_prompt": "cloud computing data center with glowing blue server racks, futuristic technology photography"},
    {"topic": "DevOps and CI/CD Pipelines: Automating the Software Lifecycle", "tag": "DevOps",
     "img_prompt": "futuristic automated pipeline visualization with glowing gears and code, cinematic tech render"},
    {"topic": "No-Code and Low-Code Platforms: Democratizing App Development", "tag": "No-Code",
     "img_prompt": "person building an app on a tablet with floating drag-and-drop interface blocks, soft futuristic lighting"},
    {"topic": "AI-Powered Chatbots: Designing Conversational Experiences", "tag": "AI & Tech",
     "img_prompt": "friendly holographic chatbot assistant floating above a smartphone, soft blue glow, cinematic"},
    {"topic": "Web3 and Blockchain Development: Building Decentralized Apps", "tag": "Web3",
     "img_prompt": "glowing blockchain network nodes connected across dark digital space, futuristic cinematic render"},
    {"topic": "Edge Computing: Processing Data Closer to the Source", "tag": "Cloud",
     "img_prompt": "network of glowing edge devices connected across a futuristic city map, cinematic blue tones"},
    {"topic": "Cybersecurity Automation: Defending Systems with AI", "tag": "Security",
     "img_prompt": "digital shield made of glowing code protecting a server, cyberpunk security concept art, cinematic"},
    {"topic": "Database Optimization Techniques for Modern Applications", "tag": "Databases",
     "img_prompt": "glowing database cylinders with flowing data streams, futuristic dark blue tech render"},
    {"topic": "Building Scalable SaaS Products from Scratch", "tag": "SaaS",
     "img_prompt": "startup team working around a glowing dashboard screen, modern tech office, cinematic warm lighting"},
    {"topic": "Machine Learning for Developers: A Practical Introduction", "tag": "AI & Tech",
     "img_prompt": "abstract neural network visualization with glowing nodes and connections, futuristic blue art, 8k"},
    {"topic": "Browser Automation and Headless Testing Explained", "tag": "Automation",
     "img_prompt": "robotic hand controlling a web browser interface, futuristic automation concept, cinematic lighting"},
    {"topic": "API Design Best Practices for Modern Applications", "tag": "APIs",
     "img_prompt": "glowing API connection diagram between devices, futuristic tech illustration, cinematic blue lighting"},
    {"topic": "The Rise of AI Coding Assistants and Pair Programming", "tag": "AI & Tech",
     "img_prompt": "developer coding alongside a friendly holographic AI assistant, warm futuristic office lighting, cinematic 8k"},
]


def load_used_topics():
    if USED_TOPICS_FILE.exists():
        try:
            with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def save_used_topic(topic_name):
    used = load_used_topics()
    used.add(topic_name)
    with open(USED_TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(used), f, indent=2, ensure_ascii=False)


def ask_ai_for_new_topic(used_titles, headers):
    """Pool exhausted -> ask the AI itself for a brand-new, never-used topic."""
    used_list_text = "\n".join(f"- {t}" for t in sorted(used_titles))
    idea_prompt = (
        "Suggest ONE brand-new blog topic idea about web development, AI, or software automation "
        "for a tech blog. It must be completely different from all topics in this list "
        "(do not repeat or reword any of them):\n"
        f"{used_list_text}\n\n"
        "Reply with ONLY this exact format, nothing else:\n"
        "TOPIC: <topic title>\n"
        "TAG: <short category tag>\n"
        "IMAGE: <6-10 word cinematic visual scene description for an AI image generator>"
    )
    payload = {"model": "meta-llama/llama-3.1-8b-instruct", "messages": [{"role": "user", "content": idea_prompt}]}
    resp = requests.post(URL, headers=headers, data=json.dumps(payload))
    text = ""
    try:
        text = resp.json()["choices"][0]["message"]["content"]
    except Exception:
        pass

    topic_match = re.search(r"TOPIC:\s*(.+)", text)
    tag_match = re.search(r"TAG:\s*(.+)", text)
    img_match = re.search(r"IMAGE:\s*(.+)", text)

    return {
        "topic": topic_match.group(1).strip() if topic_match else "New Trends in Software Development",
        "tag": tag_match.group(1).strip() if tag_match else "AI & Tech",
        "img_prompt": img_match.group(1).strip() if img_match else "futuristic glowing code on screen, cinematic 8k tech render",
    }


def pick_unused_topic(headers):
    used = load_used_topics()
    unused = [t for t in TOPICS if t["topic"] not in used]
    if unused:
        return random.choice(unused)
    print("⚠️ All fixed topics used before. Asking AI to invent a brand-new one...")
    return ask_ai_for_new_topic(used, headers)


def generate_article():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        'HTTP-Referer': 'https://codewithzaid.vercel.app/',
        'X-Title': 'CodeWithZaid'
    }

    selected = pick_unused_topic(headers)
    topic = selected["topic"]
    category = selected["tag"]
    img_prompt = selected["img_prompt"]

    prompt_text = (
        f"You are a professional tech writer. Write an engaging, in-depth article about '{topic}'.\n\n"
        "STRICT RULES:\n"
        "1. Content must be 100% original and unique — never copy phrasing from any real article.\n"
        "2. Structure with a single <h1> main title, clear <h2> subheadings, and detailed <p> paragraphs.\n"
        "3. Do not write markdown ticks or hashes — raw HTML only.\n\n"
        "OUTPUT FORMAT — reply with EXACTLY this structure, nothing else:\n"
        "TITLE: <a catchy, SEO-optimized, trending-style headline for this article>\n"
        "DESCRIPTION: <one unique, compelling meta description under 160 characters for THIS article>\n"
        "---CONTENT---\n"
        "<the full raw HTML article here, starting with a single <h1> title>"
    )

    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [{"role": "user", "content": prompt_text}]
    }

    response = requests.post(URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"❌ API Error: {response.text}")
        return

    try:
        raw_text = response.json()['choices'][0]['message']['content']
    except (KeyError, IndexError):
        print("❌ Error parsing response content.")
        return

    raw_text = raw_text.replace("```html", "").replace("```", "").strip()

    title_match = re.search(r"TITLE:\s*(.+)", raw_text)
    desc_match = re.search(r"DESCRIPTION:\s*(.+)", raw_text)
    content_split = raw_text.split("---CONTENT---")

    seo_title = title_match.group(1).strip() if title_match else topic
    seo_description = desc_match.group(1).strip() if desc_match else f"A hands-on exploration into {topic}."
    content = content_split[1].strip() if len(content_split) > 1 else raw_text

    save_html_file(content, seo_title, seo_description, category, img_prompt)
    save_used_topic(topic)


# Reliable static fallback images (Unsplash) used ONLY if the Pollinations
# AI-generated image fails to load — so a card is never left blank/broken.
FALLBACK_IMAGES = {
    "ai": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=600&q=60",
    "data": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=600&q=60",
    "generic": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=600&q=60",
}


def get_fallback_image(category):
    cat = category.lower()
    if any(k in cat for k in ["ai", "security", "machine", "ml"]):
        return FALLBACK_IMAGES["ai"]
    if any(k in cat for k in ["scraping", "database", "api"]):
        return FALLBACK_IMAGES["data"]
    return FALLBACK_IMAGES["generic"]


def update_blog_listing(today, title, description, category, img_prompt):
    blog_page_path = str(BASE_DIR / "blog.html")
    if not os.path.exists(blog_page_path):
        return

    with open(blog_page_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    blog_grid = soup.find("div", class_="card-grid") or soup.find("div", class_="blog-grid")
    if blog_grid:
        # If a card for today already exists (e.g. a manual re-run), remove the
        # OLD one first so it gets replaced with fresh title/description/image
        # instead of being silently skipped.
        existing_link = blog_grid.find("a", href=f"blog/{today}.html")
        if existing_link:
            existing_article = existing_link.find_parent("article", class_="card")
            if existing_article:
                existing_article.decompose()

        new_card = soup.new_tag("article", **{"class": "card"})

        prompt_encoded = urllib.parse.quote(img_prompt)
        random_seed = random.randint(1, 9999)
        dynamic_img_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=600&height=350&nologo=true&seed={random_seed}"
        fallback_img_url = get_fallback_image(category)

        card_content = f"""
          <div class="card-img-wrapper">
            <img src="{dynamic_img_url}" alt="{title}" loading="lazy" onerror="this.onerror=null;this.src='{fallback_img_url}';">
          </div>
          <div class="card-topic-box">
            <span class="topic-title">{category}</span>
          </div>
          <div class="card-body">
            <h3>{title}</h3>
            <p>{description}</p>
            <div class="card-action">
              <a href="blog/{today}.html" class="read-btn">Read More →</a>
            </div>
          </div>
        """
        new_card.append(BeautifulSoup(card_content, "html.parser"))
        blog_grid.insert(0, new_card)

        with open(blog_page_path, "w", encoding="utf-8") as f:
            f.write(str(soup))


def save_html_file(content, title, description, category, img_prompt):
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(BASE_DIR / "blog", exist_ok=True)
    filename = str(BASE_DIR / "blog" / f"{today}.html")

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title} — CodeWithZaid</title>
    <link rel="stylesheet" href="../style.css">
    <script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
    <div class="reading-progress" id="readingProgress"></div>

    <header class="site-header">
      <nav class="nav wrap" aria-label="Primary">
        <a href="../index.html" class="logo"><span class="bracket">&lt;</span>CodeWithZaid<span class="bracket">/&gt;</span></a>
        <ul class="nav-links">
          <li><a href="../index.html">Home</a></li>
          <li><a href="../blog.html">Blog</a></li>
          <li><a href="../about.html">About</a></li>
          <li><a href="../contact.html">Contact</a></li>
          <li><a class="nav-external-link" href="https://echoes-of-history-two.vercel.app/" target="_blank" rel="noopener">History Blog ↗</a></li>
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

    <script>
      // Reading progress bar
      window.addEventListener("scroll", function () {{
        var bar = document.getElementById("readingProgress");
        if (!bar) return;
        var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
        var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        var pct = height > 0 ? (scrollTop / height) * 100 : 0;
        bar.style.width = pct + "%";
      }});
    </script>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)

    update_blog_listing(today, title, description, category, img_prompt)


if __name__ == "__main__":
    generate_article()
