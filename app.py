# SEO Bot - Full Version with AI Generation & Stripe
import os
import json
from datetime import datetime
from openai import OpenAI
from flask import Flask, request, jsonify, render_template_string, redirect
import stripe
from keyword_research import keyword_bp
from competitor_analysis import competitor_bp
import json

# Initialize
app = Flask(__name__)
app.register_blueprint(keyword_bp, url_prefix='/keyword')
app.register_blueprint(competitor_bp, url_prefix='/competitor')

# AI Export Hub Data
AI_TOOLS_DATA = [
    {"id": 1, "name": "SEO Bot", "category": "AI Marketing", "description": "AI-powered SEO article generator. Rank higher in minutes.", "features": ["Keyword optimization", "Auto formatting", "Multi-language"], "price": "$29/mo", "website": "https://seo-bot-qrk9.onrender.com", "rating": 4.8, "reviews": 128, "tags": ["SEO", "Content", "AI Writing"]},
    {"id": 2, "name": "Shopify Magic", "category": "AI Store Builder", "description": "Shopify's official AI tool for product descriptions and marketing copy.", "features": ["Product descriptions", "Email marketing", "Ad copy"], "price": "Free (Shopify users)", "website": "https://www.shopify.com/magic", "rating": 4.5, "reviews": 256, "tags": ["Shopify", "E-commerce", "AI Copy"]},
    {"id": 3, "name": "DeepL Pro", "category": "AI Translation", "description": "Professional AI translation supporting 31 languages with high accuracy.", "features": ["Document translation", "API integration", "Glossary"], "price": "$8.99/mo", "website": "https://www.deepl.com/pro", "rating": 4.9, "reviews": 512, "tags": ["Translation", "Localization", "API"]},
    {"id": 4, "name": "Jasper AI", "category": "AI Writing", "description": "Enterprise-grade AI writing assistant for marketing teams.", "features": ["Blog posts", "Social media", "Ad copy", "Email campaigns"], "price": "$49/mo", "website": "https://www.jasper.ai", "rating": 4.7, "reviews": 890, "tags": ["AI Writing", "Marketing", "Enterprise"]},
    {"id": 5, "name": "ChatGPT API", "category": "AI Customer Service", "description": "OpenAI's API for building custom AI customer service solutions.", "features": ["Custom chatbots", "API access", "Fine-tuning", "Scalable"], "price": "Pay per use", "website": "https://openai.com/api", "rating": 4.8, "reviews": 2100, "tags": ["API", "Chatbot", "Automation"]},
    {"id": 6, "name": "Copy.ai", "category": "AI Marketing", "description": "AI copywriting tool for e-commerce product descriptions and ads.", "features": ["Product descriptions", "Ad copy", "Social posts", "Blog ideas"], "price": "$36/mo", "website": "https://www.copy.ai", "rating": 4.6, "reviews": 670, "tags": ["Copywriting", "E-commerce", "Marketing"]},
    {"id": 7, "name": "AfterShip", "category": "AI Logistics", "description": "AI-powered shipment tracking and delivery notifications.", "features": ["Multi-carrier tracking", "AI predictions", "Branded notifications", "Analytics"], "price": "$9/mo", "website": "https://www.aftership.com", "rating": 4.7, "reviews": 420, "tags": ["Logistics", "Tracking", "Notifications"]},
    {"id": 8, "name": "Stripe", "category": "AI Payment", "description": "Global payment platform with AI fraud detection.", "features": ["Global payments", "AI fraud detection", "Subscriptions", "Invoicing"], "price": "2.9% + 30¢ per transaction", "website": "https://stripe.com", "rating": 4.9, "reviews": 3500, "tags": ["Payment", "Fraud Detection", "Global"]}
]

AI_CATEGORIES = list(set(tool["category"] for tool in AI_TOOLS_DATA))

# API Keys
openai_api_key = os.getenv("OPENAI_API_KEY", "")
stripe_api_key = os.getenv("STRIPE_API_KEY", "")

client = OpenAI(api_key=openai_api_key) if openai_api_key else None
stripe.api_key = stripe_api_key.strip() if stripe_api_key else ""

# Google Tag for Ads tracking
GOOGLE_TAG = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18029847499"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', 'AW-18029847499');
</script>
"""

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SEO Bot - AI Article Generator</title>
    """ + GOOGLE_TAG + """
    <style>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #333; text-align: center; }
        .pricing { display: flex; gap: 20px; margin: 30px 0; flex-wrap: wrap; }
        .plan { flex: 1; min-width: 250px; padding: 20px; border: 2px solid #ddd; border-radius: 10px; text-align: center; background: white; }
        .plan.featured { border-color: #007bff; transform: scale(1.05); }
        .price { font-size: 2.5em; color: #007bff; font-weight: bold; }
        button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px; }
        button:hover { background: #0056b3; }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
        .result { margin-top: 30px; padding: 20px; background: white; border-radius: 5px; border-left: 4px solid #007bff; }
        .article { white-space: pre-wrap; line-height: 1.6; }
        .success { color: green; font-weight: bold; }
        .error { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>SEO Bot</h1>
    <p style="text-align: center; font-size: 18px; color: #666;">AI-powered SEO article generator. Rank higher in minutes.</p>
    
    <div class="pricing">
        <div class="plan">
            <h3>Starter</h3>
            <div class="price">$29/mo</div>
            <p>10 articles/month</p>
            <button onclick="window.location.href='/checkout?plan=starter'">Get Started</button>
        </div>
        <div class="plan featured">
            <h3>Pro</h3>
            <div class="price">$79/mo</div>
            <p>50 articles/month</p>
            <button onclick="window.location.href='/checkout?plan=pro'">Most Popular</button>
        </div>
        <div class="plan">
            <h3>Enterprise</h3>
            <div class="price">$199/mo</div>
            <p>Unlimited articles</p>
            <button onclick="window.location.href='/checkout?plan=enterprise'">Contact Us</button>
        </div>
    </div>
    
    <h2 style="text-align: center; margin-top: 40px;"><a href="/keyword" style="color: #007bff;">Try Keyword Research Tool</a></h2>
    <h2 style="text-align: center; margin-top: 20px;"><a href="/competitor" style="color: #28a745;">Try Competitor Analysis</a></h2>
    <h2 style="text-align: center; margin-top: 20px;"><a href="/ai-tools" style="color: #764ba2;">🚀 Explore AI Export Hub (8 AI Tools)</a></h2>
    
    <h2 style="text-align: center; margin-top: 40px;">Try Free - Generate Article</h2>
    <form id="generateForm">
        <div class="form-group">
            <label>Keyword / Topic:</label>
            <input type="text" id="keyword" placeholder="e.g., best coffee maker 2025" required>
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
    
    <div id="result" style="display:none;"></div>
    
    <script>
        document.getElementById('generateForm').onsubmit = async (e) => {
            e.preventDefault();
            const btn = document.querySelector('button[type="submit"]');
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
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            
            if (data.error) {
                resultDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            } else {
                resultDiv.innerHTML = `
                    <h3>${data.title}</h3>
                    <div class="article">${data.content}</div>
                    <p class="success">Word count: ${data.word_count}</p>
                `;
            }
            btn.textContent = 'Generate Article';
        };
    </script>
</body>
</html>
"""

def generate_article(keyword: str, length: str = "medium"):
    """Generate SEO-optimized article using OpenAI"""
    if not client:
        return {"error": "OpenAI API not configured"}
    
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
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content
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
        return {"error": str(e)}

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

@app.route('/checkout')
def checkout():
    """Stripe checkout"""
    plan = request.args.get('plan', 'starter')
    
    prices = {
        'starter': {'price': 2900, 'name': 'SEO Bot Starter'},
        'pro': {'price': 7900, 'name': 'SEO Bot Pro'},
        'enterprise': {'price': 19900, 'name': 'SEO Bot Enterprise'}
    }
    
    plan_data = prices.get(plan, prices['starter'])
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': plan_data['name']},
                    'unit_amount': plan_data['price'],
                    'recurring': {'interval': 'month'}
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.host_url + 'success',
            cancel_url=request.host_url + 'cancel',
        )
        return redirect(session.url, code=303)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/success')
def success():
    return "<h1>Payment Successful!</h1><p>Welcome to SEO Bot!</p><a href='/'>Go to Dashboard</a>"

@app.route('/cancel')
def cancel():
    return "<h1>Payment Cancelled</h1><p>You can try again anytime.</p><a href='/'>Go Back</a>"

# AI Export Hub Routes
@app.route('/ai-tools')
def ai_tools_home():
    """AI Export Hub Home"""
    return render_template_string(AI_TOOLS_TEMPLATE, tools=AI_TOOLS_DATA, categories=AI_CATEGORIES, total_tools=len(AI_TOOLS_DATA))

@app.route('/ai-tools/tool/<int:tool_id>')
def ai_tool_detail(tool_id):
    """AI Tool Detail Page"""
    tool = next((t for t in AI_TOOLS_DATA if t['id'] == tool_id), None)
    if not tool:
        return "Tool not found", 404
    return render_template_string(AI_TOOL_DETAIL_TEMPLATE, tool=tool)

@app.route('/ai-tools/category/<category>')
def ai_tools_category(category):
    """AI Tools by Category"""
    filtered_tools = [t for t in AI_TOOLS_DATA if t['category'] == category]
    return render_template_string(AI_TOOLS_CATEGORY_TEMPLATE, tools=filtered_tools, category=category)

# AI Export Hub Templates
AI_TOOLS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Export Hub - Cross-border E-commerce AI Tools</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f7fa; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; border-radius: 10px; margin-bottom: 30px; }
        .header h1 { margin: 0; font-size: 2.5em; }
        .stats { display: flex; justify-content: center; gap: 40px; margin-top: 20px; }
        .stat { text-align: center; }
        .stat-number { font-size: 2em; font-weight: bold; }
        .tools-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .tool-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-decoration: none; color: inherit; }
        .tool-card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.15); }
        .tool-name { font-size: 1.3em; font-weight: bold; color: #333; margin-bottom: 10px; }
        .tool-category { background: #f0f0f0; padding: 5px 10px; border-radius: 15px; font-size: 0.8em; color: #666; }
        .tool-description { color: #666; margin: 10px 0; }
        .tool-price { color: #667eea; font-weight: bold; }
        .nav { text-align: center; margin-bottom: 20px; }
        .nav a { margin: 0 10px; color: #667eea; text-decoration: none; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Export Hub</h1>
        <p>AI-powered tools for cross-border e-commerce</p>
        <div class="stats">
            <div class="stat"><div class="stat-number">{{ total_tools }}</div><div>AI Tools</div></div>
            <div class="stat"><div class="stat-number">{{ categories|length }}</div><div>Categories</div></div>
        </div>
    </div>
    <div class="nav">
        <a href="/">← Back to SEO Bot</a>
    </div>
    <div class="tools-grid">
        {% for tool in tools %}
        <a href="/ai-tools/tool/{{ tool.id }}" class="tool-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span class="tool-name">{{ tool.name }}</span>
                <span class="tool-category">{{ tool.category }}</span>
            </div>
            <div class="tool-description">{{ tool.description }}</div>
            <div class="tool-price">{{ tool.price }}</div>
            <div style="margin-top:10px;color:#ffa500;">⭐ {{ tool.rating }} ({{ tool.reviews }})</div>
        </a>
        {% endfor %}
    </div>
</body>
</html>
'''

AI_TOOL_DETAIL_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ tool.name }} - AI Export Hub</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f7fa; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .header a { color: white; text-decoration: none; }
        .content { background: white; padding: 30px; border-radius: 10px; }
        .tool-title { font-size: 2em; margin-bottom: 10px; }
        .tool-category { background: #f0f0f0; padding: 5px 15px; border-radius: 20px; display: inline-block; margin-bottom: 20px; }
        .tool-description { font-size: 1.2em; color: #555; margin-bottom: 20px; }
        .features { list-style: none; padding: 0; }
        .features li { padding: 10px 0; border-bottom: 1px solid #eee; }
        .features li:before { content: "✓"; color: #4caf50; font-weight: bold; margin-right: 10px; }
        .cta { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; margin-top: 30px; }
        .cta a { background: white; color: #667eea; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="header">
        <a href="/ai-tools">← Back to AI Tools</a>
    </div>
    <div class="content">
        <h1 class="tool-title">{{ tool.name }}</h1>
        <span class="tool-category">{{ tool.category }}</span>
        <div style="color:#ffa500;margin:15px 0;">⭐ {{ tool.rating }} ({{ tool.reviews }} reviews)</div>
        <p class="tool-description">{{ tool.description }}</p>
        <h3>Key Features</h3>
        <ul class="features">
            {% for feature in tool.features %}<li>{{ feature }}</li>{% endfor %}
        </ul>
        <div class="cta">
            <div style="font-size:2em;font-weight:bold;">{{ tool.price }}</div>
            <a href="{{ tool.website }}" target="_blank">Visit Website</a>
        </div>
    </div>
</body>
</html>
'''

AI_TOOLS_CATEGORY_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ category }} - AI Export Hub</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f7fa; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; border-radius: 10px; margin-bottom: 30px; }
        .header a { color: white; position: absolute; left: 20px; }
        .tools-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .tool-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-decoration: none; color: inherit; }
    </style>
</head>
<body>
    <div class="header">
        <a href="/ai-tools">← Back</a>
        <h1>{{ category }}</h1>
        <p>{{ tools|length }} tools found</p>
    </div>
    <div class="tools-grid">
        {% for tool in tools %}
        <a href="/ai-tools/tool/{{ tool.id }}" class="tool-card">
            <h3>{{ tool.name }}</h3>
            <p>{{ tool.description }}</p>
            <div style="color:#667eea;font-weight:bold;">{{ tool.price }}</div>
        </a>
        {% endfor %}
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
