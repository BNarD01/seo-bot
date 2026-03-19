# SEO BOT - AI SEO Article Generator
# Minimal viable product - ready to launch

import os
import json
import time
from datetime import datetime
from openai import OpenAI
from flask import Flask, request, jsonify, render_template_string

# Initialize
app = Flask(__name__)

# Use Kimi API (more stable)
client = OpenAI(
    api_key=os.getenv("KIMI_API_KEY", ""),
    base_url="https://api.moonshot.cn/v1"
)

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SEO Bot - AI Article Generator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 5px; }
        .pricing { display: flex; gap: 20px; margin: 30px 0; }
        .plan { flex: 1; padding: 20px; border: 2px solid #ddd; border-radius: 10px; text-align: center; }
        .plan.featured { border-color: #007bff; }
        .price { font-size: 2em; color: #007bff; }
    </style>
</head>
<body>
    <h1>SEO Bot</h1>
    <p>AI-powered SEO article generator. Rank higher in 3 minutes.</p>
    
    <div class="pricing">
        <div class="plan">
            <h3>Starter</h3>
            <div class="price">$29/mo</div>
            <p>10 articles/month</p>
        </div>
        <div class="plan featured">
            <h3>Pro</h3>
            <div class="price">$79/mo</div>
            <p>50 articles/month</p>
        </div>
        <div class="plan">
            <h3>Enterprise</h3>
            <div class="price">$199/mo</div>
            <p>Unlimited</p>
        </div>
    </div>
    
    <h2>Try Free</h2>
    <form id="generateForm">
        <div class="form-group">
            <label>Keyword / Topic:</label>
            <input type="text" id="keyword" placeholder="e.g., best coffee maker 2024" required>
        </div>
        <div class="form-group">
            <label>Article Length:</label>
            <select id="length">
                <option value="short">Short (500 words)</option>
                <option value="medium" selected>Medium (1000 words)</option>
                <option value="long">Long (2000 words)</option>
            </select>
        </div>
        <button type="submit">Generate Article</button>
    </form>
    
    <div id="result" class="result" style="display:none;"></div>
    
    <script>
        document.getElementById('generateForm').onsubmit = async (e) => {
            e.preventDefault();
            const btn = document.querySelector('button');
            btn.textContent = 'Generating...';
            
            const res = await fetch('/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    keyword: document.getElementById('keyword').value,
                    length: document.getElementById('length').value
                })
            });
            
            const data = await res.json();
            document.getElementById('result').style.display = 'block';
            document.getElementById('result').innerHTML = `
                <h3>${data.title}</h3>
                <pre style="white-space: pre-wrap;">${data.content}</pre>
            `;
            btn.textContent = 'Generate Article';
        };
    </script>
</body>
</html>
"""

def generate_article(keyword: str, length: str = "medium") -> dict:
    """Generate SEO-optimized article using OpenAI"""
    
    length_words = {"short": 500, "medium": 1000, "long": 2000}
    target_words = length_words.get(length, 1000)
    
    prompt = f"""Write a SEO-optimized blog article about "{keyword}".

Requirements:
- Target length: {target_words} words
- Include H1, H2, H3 headings
- Include meta description
- Include 3-5 relevant keywords naturally
- Write in engaging, informative style
- Include introduction and conclusion
- Use bullet points where appropriate

Format:
TITLE: [SEO-optimized title]
META: [Meta description under 160 chars]
KEYWORDS: [comma-separated keywords]

[Article content with proper headings]
"""
    
    try:
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content
        
        # Parse response
        lines = content.split('\n')
        title = lines[0].replace('TITLE:', '').strip() if lines[0].startswith('TITLE:') else f"Complete Guide to {keyword}"
        
        return {
            "title": title,
            "content": content,
            "keyword": keyword,
            "word_count": len(content.split()),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "title": f"Error generating article about {keyword}"
        }

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    keyword = data.get('keyword', '')
    length = data.get('length', 'medium')
    
    if not keyword:
        return jsonify({"error": "Keyword required"}), 400
    
    result = generate_article(keyword, length)
    return jsonify(result)

@app.route('/api/keywords', methods=['POST'])
def research_keywords():
    """Keyword research endpoint"""
    data = request.json
    seed = data.get('seed', '')
    
    prompt = f"""Generate 10 SEO keywords related to "{seed}" with search intent:
    Format: keyword | intent (informational/commercial/transactional) | difficulty (easy/medium/hard)
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return jsonify({
            "seed": seed,
            "keywords": response.choices[0].message.content,
            "generated_at": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("SEO Bot starting...")
    print("Open http://localhost:5000 in your browser")
    app.run(host='0.0.0.0', port=5000, debug=True)
