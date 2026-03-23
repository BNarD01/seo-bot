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

# HTML Template - Combined SEO Bot + AI Export Hub
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Bot + AI Export Hub - AI Tools for E-commerce</title>
    """ + GOOGLE_TAG + """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: #f8f9fa; color: #333; }
        .container { max-width: 1400px; margin: 0 auto; padding: 0 20px; }
        
        /* Hero Section */
        .hero { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 80px 20px;
            text-align: center;
        }
        .hero h1 { font-size: 3.5em; font-weight: 700; margin-bottom: 20px; }
        .hero p { font-size: 1.3em; opacity: 0.9; max-width: 600px; margin: 0 auto 30px; }
        .hero-badges { display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; margin-top: 40px; }
        .hero-badge { 
            background: rgba(255,255,255,0.15); 
            backdrop-filter: blur(10px);
            padding: 20px 40px; 
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .hero-badge-number { font-size: 2.5em; font-weight: 700; display: block; }
        .hero-badge-label { font-size: 0.95em; opacity: 0.9; }
        
        /* Section Styles */
        .section { padding: 60px 0; }
        .section-title { 
            font-size: 2.2em; 
            font-weight: 700; 
            text-align: center; 
            margin-bottom: 50px;
            color: #333;
        }
        .section-subtitle {
            text-align: center;
            color: #666;
            font-size: 1.1em;
            margin-top: -40px;
            margin-bottom: 50px;
        }
        
        /* Pricing */
        .pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; max-width: 1000px; margin: 0 auto; }
        .pricing-card { 
            background: white; 
            padding: 40px 30px; 
            border-radius: 20px; 
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        .pricing-card:hover { transform: translateY(-5px); box-shadow: 0 10px 40px rgba(0,0,0,0.12); }
        .pricing-card.featured { 
            border-color: #667eea; 
            transform: scale(1.05);
            position: relative;
        }
        .pricing-card.featured::before {
            content: 'MOST POPULAR';
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 20px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 700;
        }
        .pricing-card h3 { font-size: 1.5em; margin-bottom: 15px; }
        .pricing-card .price { 
            font-size: 3em; 
            font-weight: 700; 
            color: #667eea;
            margin: 20px 0;
        }
        .pricing-card button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 30px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        .pricing-card button:hover { transform: scale(1.05); box-shadow: 0 5px 20px rgba(102,126,234,0.4); }
        
        /* AI Tools Section */
        .ai-tools-section { background: linear-gradient(135deg, #f8f9ff 0%, #fff 100%); }
        .tools-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); 
            gap: 25px;
        }
        .tool-card { 
            background: white; 
            padding: 30px; 
            border-radius: 20px; 
            box-shadow: 0 4px 15px rgba(102,126,234,0.08);
            text-decoration: none; 
            color: inherit;
            transition: all 0.3s ease;
            border: 1px solid rgba(102,126,234,0.1);
        }
        .tool-card:hover { 
            transform: translateY(-8px); 
            box-shadow: 0 20px 40px rgba(102,126,234,0.15);
            border-color: rgba(102,126,234,0.3);
        }
        .tool-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px; }
        .tool-card-name { font-size: 1.3em; font-weight: 700; color: #333; }
        .tool-card-category { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.7em;
            font-weight: 600;
            text-transform: uppercase;
        }
        .tool-card-desc { color: #666; margin-bottom: 15px; line-height: 1.5; }
        .tool-card-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 15px; }
        .tool-card-price { color: #667eea; font-weight: 700; font-size: 1.1em; }
        .tool-card-rating { color: #ffa500; font-weight: 600; }
        
        /* Generator Section */
        .generator-section { background: white; }
        .generator-box {
            max-width: 700px;
            margin: 0 auto;
            background: linear-gradient(145deg, #f8f9ff 0%, #ffffff 100%);
            padding: 50px;
            border-radius: 25px;
            box-shadow: 0 10px 40px rgba(102,126,234,0.1);
        }
        .form-group { margin-bottom: 25px; }
        .form-group label { display: block; margin-bottom: 10px; font-weight: 600; color: #333; }
        .form-group input, .form-group select {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        .generate-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 18px 50px;
            border-radius: 30px;
            font-size: 1.1em;
            font-weight: 700;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
        }
        .generate-btn:hover { transform: scale(1.02); box-shadow: 0 10px 30px rgba(102,126,234,0.4); }
        
        /* Tools Links */
        .tools-links { display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; margin: 40px 0; }
        .tools-links a {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 15px 30px;
            background: white;
            border-radius: 12px;
            text-decoration: none;
            color: #333;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        .tools-links a:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.12); }
        .tools-links a.keyword { color: #007bff; }
        .tools-links a.competitor { color: #28a745; }
        
        /* Result */
        .result-box {
            margin-top: 30px;
            padding: 30px;
            background: white;
            border-radius: 15px;
            border-left: 4px solid #667eea;
            display: none;
        }
        .result-box.show { display: block; }
        
        /* Footer */
        .footer {
            background: #333;
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.2em; }
            .hero-badges { flex-direction: column; align-items: center; }
            .pricing-card.featured { transform: scale(1); }
            .tools-grid { grid-template-columns: 1fr; }
            .generator-box { padding: 30px 20px; }
        }
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1>SEO Bot + AI Export Hub</h1>
            <p>All-in-one AI toolkit for cross-border e-commerce. Generate SEO content and discover AI tools to scale your business.</p>
            <div class="hero-badges">
                <div class="hero-badge">
                    <span class="hero-badge-number">8</span>
                    <span class="hero-badge-label">AI Tools</span>
                </div>
                <div class="hero-badge">
                    <span class="hero-badge-number">3</span>
                    <span class="hero-badge-label">SEO Tools</span>
                </div>
                <div class="hero-badge">
                    <span class="hero-badge-number">1000+</span>
                    <span class="hero-badge-label">Active Users</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Pricing Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Choose Your Plan</h2>
            <p class="section-subtitle">Start generating SEO-optimized articles in minutes</p>
            <div class="pricing-grid">
                <div class="pricing-card">
                    <h3>Starter</h3>
                    <div class="price">$29/mo</div>
                    <p>10 articles/month</p>
                    <button onclick="window.location.href='/checkout?plan=starter'">Get Started</button>
                </div>
                <div class="pricing-card featured">
                    <h3>Pro</h3>
                    <div class="price">$79/mo</div>
                    <p>50 articles/month</p>
                    <button onclick="window.location.href='/checkout?plan=pro'">Most Popular</button>
                </div>
                <div class="pricing-card">
                    <h3>Enterprise</h3>
                    <div class="price">$199/mo</div>
                    <p>Unlimited articles</p>
                    <button onclick="window.location.href='/checkout?plan=enterprise'">Contact Us</button>
                </div>
            </div>
        </div>
    </section>

    <!-- AI Tools Section -->
    <section class="section ai-tools-section">
        <div class="container">
            <h2 class="section-title">Featured AI Tools</h2>
            <p class="section-subtitle">Discover AI-powered tools to boost your e-commerce business</p>
            <div class="tools-grid">
                {% for tool in ai_tools[:6] %}
                <a href="/ai-tools/tool/{{ tool.id }}" class="tool-card">
                    <div class="tool-card-header">
                        <span class="tool-card-name">{{ tool.name }}</span>
                        <span class="tool-card-category">{{ tool.category }}</span>
                    </div>
                    <div class="tool-card-desc">{{ tool.description }}</div>
                    <div class="tool-card-footer">
                        <span class="tool-card-price">{{ tool.price }}</span>
                        <span class="tool-card-rating">⭐ {{ tool.rating }}</span>
                    </div>
                </a>
                {% endfor %}
            </div>
            <div style="text-align: center; margin-top: 40px;">
                <a href="/ai-tools" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: 600;">View All 8 AI Tools →</a>
            </div>
        </div>
    </section>

    <!-- Generator Section -->
    <section class="section generator-section">
        <div class="container">
            <h2 class="section-title">Try Free - Generate Article</h2>
            <p class="section-subtitle">Enter a keyword and get an SEO-optimized article instantly</p>
            
            <div class="tools-links">
                <a href="/keyword" class="keyword">🔍 Keyword Research Tool</a>
                <a href="/competitor" class="competitor">📊 Competitor Analysis</a>
            </div>
            
            <div class="generator-box">
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
                    <button type="submit" class="generate-btn">Generate Article</button>
                </form>
                <div id="result" class="result-box"></div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>© 2025 SEO Bot + AI Export Hub. Empowering e-commerce sellers worldwide.</p>
        </div>
    </footer>
    
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
    """AI Export Hub as homepage"""
    return render_template_string(AI_TOOLS_HOMEPAGE_TEMPLATE, tools=AI_TOOLS_DATA, categories=AI_CATEGORIES, total_tools=len(AI_TOOLS_DATA))

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
@app.route('/seo-bot')
def seo_bot_page():
    """SEO Bot Article Generator Page"""
    return render_template_string(SEO_BOT_TEMPLATE)

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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Export Hub - Cross-border E-commerce AI Tools Directory</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 40px 20px; }
        .nav { 
            background: rgba(255,255,255,0.1); 
            backdrop-filter: blur(10px);
            padding: 15px 30px; 
            border-radius: 50px; 
            display: inline-block; 
            margin-bottom: 30px;
        }
        .nav a { 
            color: white; 
            text-decoration: none; 
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .nav a:hover { opacity: 0.8; }
        .header { 
            text-align: center; 
            color: white; 
            padding: 60px 20px;
        }
        .header h1 { 
            font-size: 4em; 
            font-weight: 700; 
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .header p { 
            font-size: 1.3em; 
            opacity: 0.9; 
            max-width: 600px;
            margin: 0 auto;
        }
        .stats { 
            display: flex; 
            justify-content: center; 
            gap: 60px; 
            margin-top: 40px;
        }
        .stat { 
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 25px 40px;
            border-radius: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .stat-number { 
            font-size: 3em; 
            font-weight: 700; 
            display: block;
        }
        .stat-label { 
            font-size: 1em; 
            opacity: 0.9;
            margin-top: 5px;
        }
        .content { 
            background: white; 
            border-radius: 30px; 
            padding: 50px;
            margin-top: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .section-title {
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 30px;
            color: #333;
        }
        .tools-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); 
            gap: 25px; 
        }
        .tool-card { 
            background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
            padding: 30px; 
            border-radius: 20px; 
            box-shadow: 0 4px 15px rgba(102,126,234,0.1);
            text-decoration: none; 
            color: inherit; 
            transition: all 0.3s ease;
            border: 1px solid rgba(102,126,234,0.1);
            position: relative;
            overflow: hidden;
        }
        .tool-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        .tool-card:hover { 
            transform: translateY(-8px); 
            box-shadow: 0 20px 40px rgba(102,126,234,0.2);
        }
        .tool-card:hover::before {
            transform: scaleX(1);
        }
        .tool-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        .tool-name { 
            font-size: 1.4em; 
            font-weight: 700; 
            color: #333;
            flex: 1;
        }
        .tool-category { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6px 14px; 
            border-radius: 20px; 
            font-size: 0.75em; 
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .tool-description { 
            color: #666; 
            margin: 15px 0;
            line-height: 1.6;
            font-size: 0.95em;
        }
        .tool-features {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 15px 0;
        }
        .feature-tag {
            background: #f0f4ff;
            color: #667eea;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 500;
        }
        .tool-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }
        .tool-price { 
            font-size: 1.2em;
            font-weight: 700;
            color: #667eea;
        }
        .tool-rating {
            display: flex;
            align-items: center;
            gap: 5px;
            color: #ffa500;
            font-weight: 600;
        }
        .cta-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px;
            border-radius: 20px;
            text-align: center;
            margin-top: 50px;
        }
        .cta-section h2 {
            font-size: 2.5em;
            margin-bottom: 15px;
        }
        .cta-section p {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        .cta-button {
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 18px 50px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1em;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .cta-button:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        @media (max-width: 768px) {
            .header h1 { font-size: 2.5em; }
            .stats { flex-direction: column; gap: 20px; }
            .tools-grid { grid-template-columns: 1fr; }
            .content { padding: 30px 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">← Back to SEO Bot</a>
        </div>
        
        <div class="header">
            <h1>AI Export Hub</h1>
            <p>Discover AI-powered tools to scale your cross-border e-commerce business globally</p>
            <div class="stats">
                <div class="stat">
                    <span class="stat-number">{{ total_tools }}</span>
                    <span class="stat-label">AI Tools</span>
                </div>
                <div class="stat">
                    <span class="stat-number">{{ categories|length }}</span>
                    <span class="stat-label">Categories</span>
                </div>
                <div class="stat">
                    <span class="stat-number">1000+</span>
                    <span class="stat-label">Active Users</span>
                </div>
            </div>
        </div>
        
        <div class="content">
            <h2 class="section-title">Featured AI Tools</h2>
            <div class="tools-grid">
                {% for tool in tools %}
                <a href="/ai-tools/tool/{{ tool.id }}" class="tool-card">
                    <div class="tool-header">
                        <span class="tool-name">{{ tool.name }}</span>
                        <span class="tool-category">{{ tool.category }}</span>
                    </div>
                    <div class="tool-description">{{ tool.description }}</div>
                    <div class="tool-features">
                        {% for feature in tool.features[:3] %}
                        <span class="feature-tag">{{ feature }}</span>
                        {% endfor %}
                    </div>
                    <div class="tool-footer">
                        <span class="tool-price">{{ tool.price }}</span>
                        <div class="tool-rating">⭐ {{ tool.rating }}</div>
                    </div>
                </a>
                {% endfor %}
            </div>
            
            <div class="cta-section">
                <h2>Have an AI tool to share?</h2>
                <p>Submit your tool and reach thousands of e-commerce sellers</p>
                <a href="mailto:submit@aiexporthub.com" class="cta-button">Submit Your Tool</a>
            </div>
        </div>
    </div>
</body>
</html>
'''

AI_TOOL_DETAIL_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ tool.name }} - AI Export Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        .nav { 
            background: rgba(255,255,255,0.1); 
            backdrop-filter: blur(10px);
            padding: 15px 30px; 
            border-radius: 50px; 
            display: inline-block; 
            margin-bottom: 30px;
        }
        .nav a { 
            color: white; 
            text-decoration: none; 
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .content { 
            background: white; 
            border-radius: 30px; 
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .tool-header {
            text-align: center;
            padding-bottom: 40px;
            border-bottom: 2px solid #f0f0f0;
            margin-bottom: 40px;
        }
        .tool-category { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 20px; 
            border-radius: 25px; 
            font-size: 0.85em; 
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: inline-block;
            margin-bottom: 20px;
        }
        .tool-title { 
            font-size: 3em; 
            font-weight: 700; 
            color: #333;
            margin-bottom: 15px;
        }
        .tool-rating {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            font-size: 1.2em;
            color: #ffa500;
        }
        .tool-description { 
            font-size: 1.3em; 
            color: #555; 
            line-height: 1.8;
            text-align: center;
            max-width: 700px;
            margin: 30px auto;
        }
        .section {
            margin: 40px 0;
        }
        .section-title {
            font-size: 1.5em;
            font-weight: 700;
            color: #333;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
        }
        .feature-item {
            background: linear-gradient(145deg, #f8f9ff 0%, #ffffff 100%);
            padding: 20px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
            border: 1px solid rgba(102,126,234,0.1);
        }
        .feature-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2em;
        }
        .feature-text {
            font-weight: 600;
            color: #333;
        }
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .tag {
            background: #f0f4ff;
            color: #667eea;
            padding: 8px 18px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }
        .cta-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px;
            border-radius: 25px;
            text-align: center;
            margin-top: 50px;
        }
        .price-display {
            font-size: 3.5em;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .price-label {
            font-size: 1.1em;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        .cta-button {
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 20px 60px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.2em;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .cta-button:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        @media (max-width: 768px) {
            .tool-title { font-size: 2em; }
            .content { padding: 30px 20px; }
            .features-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/ai-tools">← Back to AI Tools</a>
        </div>
        
        <div class="content">
            <div class="tool-header">
                <span class="tool-category">{{ tool.category }}</span>
                <h1 class="tool-title">{{ tool.name }}</h1>
                <div class="tool-rating">
                    <span>⭐ {{ tool.rating }}</span>
                    <span style="color:#999;">({{ tool.reviews }} reviews)</span>
                </div>
                <p class="tool-description">{{ tool.description }}</p>
            </div>
            
            <div class="section">
                <h3 class="section-title">✨ Key Features</h3>
                <div class="features-grid">
                    {% for feature in tool.features %}
                    <div class="feature-item">
                        <div class="feature-icon">✓</div>
                        <span class="feature-text">{{ feature }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="section">
                <h3 class="section-title">🏷️ Tags</h3>
                <div class="tags">
                    {% for tag in tool.tags %}
                    <span class="tag">{{ tag }}</span>
                    {% endfor %}
                </div>
            </div>
            
            <div class="cta-section">
                <div class="price-display">{{ tool.price }}</div>
                <div class="price-label">Start using {{ tool.name }} today</div>
                <a href="{{ tool.website }}" target="_blank" class="cta-button">Visit Website →</a>
            </div>
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

# AI Export Hub Homepage Template (New Main Page)
AI_TOOLS_HOMEPAGE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Export Hub - AI Tools for Cross-border E-commerce</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 40px 20px; }
        
        /* Hero Section */
        .hero { 
            text-align: center; 
            color: white; 
            padding: 60px 20px;
        }
        .hero h1 { 
            font-size: 4em; 
            font-weight: 700; 
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .hero p { 
            font-size: 1.3em; 
            opacity: 0.9; 
            max-width: 600px;
            margin: 0 auto 40px;
        }
        .stats { 
            display: flex; 
            justify-content: center; 
            gap: 60px; 
            flex-wrap: wrap;
        }
        .stat { 
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 25px 50px;
            border-radius: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .stat-number { 
            font-size: 3em; 
            font-weight: 700; 
            display: block;
        }
        .stat-label { 
            font-size: 1em; 
            opacity: 0.9;
            margin-top: 5px;
        }
        
        /* Content Section */
        .content { 
            background: white; 
            border-radius: 30px; 
            padding: 60px;
            margin-top: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .section-title { 
            font-size: 2.2em; 
            font-weight: 700; 
            text-align: center; 
            margin-bottom: 50px;
            color: #333;
        }
        
        /* Tools Grid */
        .tools-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); 
            gap: 30px;
        }
        .tool-card { 
            background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
            padding: 35px; 
            border-radius: 20px; 
            box-shadow: 0 4px 20px rgba(102,126,234,0.1);
            text-decoration: none; 
            color: inherit;
            transition: all 0.3s ease;
            border: 1px solid rgba(102,126,234,0.1);
            position: relative;
            overflow: hidden;
        }
        .tool-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        .tool-card:hover { 
            transform: translateY(-8px); 
            box-shadow: 0 20px 50px rgba(102,126,234,0.2);
        }
        .tool-card:hover::before {
            transform: scaleX(1);
        }
        .tool-card.featured {
            border: 2px solid #667eea;
            background: linear-gradient(145deg, #f0f4ff 0%, #ffffff 100%);
        }
        .tool-card.featured::after {
            content: 'OUR PRODUCT';
            position: absolute;
            top: 15px;
            right: -30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 40px;
            font-size: 0.7em;
            font-weight: 700;
            transform: rotate(45deg);
        }
        .tool-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        .tool-name { 
            font-size: 1.5em; 
            font-weight: 700; 
            color: #333;
            flex: 1;
        }
        .tool-category { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6px 14px; 
            border-radius: 20px; 
            font-size: 0.75em; 
            font-weight: 600;
            text-transform: uppercase;
        }
        .tool-description { 
            color: #666; 
            margin: 15px 0;
            line-height: 1.6;
            font-size: 1em;
        }
        .tool-features {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 15px 0;
        }
        .feature-tag {
            background: #f0f4ff;
            color: #667eea;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 500;
        }
        .tool-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }
        .tool-price { 
            font-size: 1.3em;
            font-weight: 700;
            color: #667eea;
        }
        .tool-rating {
            display: flex;
            align-items: center;
            gap: 5px;
            color: #ffa500;
            font-weight: 600;
        }
        
        /* CTA Section */
        .cta-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px;
            border-radius: 25px;
            text-align: center;
            margin-top: 60px;
        }
        .cta-section h2 {
            font-size: 2.5em;
            margin-bottom: 15px;
        }
        .cta-section p {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        .cta-button {
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 18px 50px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1em;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .cta-button:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.5em; }
            .stats { flex-direction: column; gap: 20px; }
            .tools-grid { grid-template-columns: 1fr; }
            .content { padding: 30px 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>AI Export Hub</h1>
            <p>Discover AI-powered tools to scale your cross-border e-commerce business globally</p>
            <div class="stats">
                <div class="stat">
                    <span class="stat-number">{{ total_tools }}</span>
                    <span class="stat-label">AI Tools</span>
                </div>
                <div class="stat">
                    <span class="stat-number">{{ categories|length }}</span>
                    <span class="stat-label">Categories</span>
                </div>
                <div class="stat">
                    <span class="stat-number">1000+</span>
                    <span class="stat-label">Active Users</span>
                </div>
            </div>
        </div>
        
        <div class="content">
            <h2 class="section-title">Featured AI Tools</h2>
            <div class="tools-grid">
                {% for tool in tools %}
                <a href="{% if tool.id == 1 %}/seo-bot{% else %}/ai-tools/tool/{{ tool.id }}{% endif %}" class="tool-card {% if tool.id == 1 %}featured{% endif %}">
                    <div class="tool-header">
                        <span class="tool-name">{{ tool.name }}</span>
                        <span class="tool-category">{{ tool.category }}</span>
                    </div>
                    <div class="tool-description">{{ tool.description }}</div>
                    <div class="tool-features">
                        {% for feature in tool.features[:3] %}
                        <span class="feature-tag">{{ feature }}</span>
                        {% endfor %}
                    </div>
                    <div class="tool-footer">
                        <span class="tool-price">{{ tool.price }}</span>
                        <div class="tool-rating">⭐ {{ tool.rating }}</div>
                    </div>
                </a>
                {% endfor %}
            </div>
            
            <div class="cta-section">
                <h2>Have an AI tool to share?</h2>
                <p>Submit your tool and reach thousands of e-commerce sellers</p>
                <a href="mailto:submit@aiexporthub.com" class="cta-button">Submit Your Tool</a>
            </div>
        </div>
    </div>
</body>
</html>
'''

# SEO Bot Article Generator Page Template
SEO_BOT_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Bot - AI Article Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        
        .nav { 
            background: rgba(255,255,255,0.1); 
            backdrop-filter: blur(10px);
            padding: 15px 30px; 
            border-radius: 50px; 
            display: inline-block; 
            margin-bottom: 30px;
        }
        .nav a { 
            color: white; 
            text-decoration: none; 
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .hero { 
            text-align: center; 
            color: white; 
            padding: 40px 20px;
        }
        .hero h1 { 
            font-size: 3em; 
            font-weight: 700; 
            margin-bottom: 15px;
        }
        .hero p { 
            font-size: 1.2em; 
            opacity: 0.9; 
        }
        
        .content { 
            background: white; 
            border-radius: 30px; 
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .pricing-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 40px;
        }
        .pricing-card { 
            background: linear-gradient(145deg, #f8f9ff 0%, #ffffff 100%);
            padding: 30px; 
            border-radius: 20px; 
            text-align: center;
            box-shadow: 0 4px 15px rgba(102,126,234,0.1);
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        .pricing-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(102,126,234,0.2); }
        .pricing-card.featured { 
            border-color: #667eea; 
            transform: scale(1.05);
        }
        .pricing-card h3 { font-size: 1.3em; margin-bottom: 10px; }
        .pricing-card .price { 
            font-size: 2.5em; 
            font-weight: 700; 
            color: #667eea;
            margin: 15px 0;
        }
        .pricing-card button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
        }
        .pricing-card button:hover { transform: scale(1.05); }
        
        .generator-box {
            background: linear-gradient(145deg, #f8f9ff 0%, #ffffff 100%);
            padding: 40px;
            border-radius: 20px;
            margin-top: 30px;
        }
        .form-group { margin-bottom: 25px; }
        .form-group label { display: block; margin-bottom: 10px; font-weight: 600; color: #333; }
        .form-group input, .form-group select {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        .generate-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 18px 50px;
            border-radius: 30px;
            font-size: 1.1em;
            font-weight: 700;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
        }
        .generate-btn:hover { transform: scale(1.02); box-shadow: 0 10px 30px rgba(102,126,234,0.4); }
        
        .result-box {
            margin-top: 30px;
            padding: 30px;
            background: white;
            border-radius: 15px;
            border-left: 4px solid #667eea;
            display: none;
        }
        .result-box.show { display: block; }
        .article { white-space: pre-wrap; line-height: 1.8; }
        
        .tools-links { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 30px; }
        .tools-links a {
            padding: 12px 25px;
            background: white;
            border-radius: 25px;
            text-decoration: none;
            color: #667eea;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2em; }
            .content { padding: 30px 20px; }
            .pricing-card.featured { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">← Back to AI Export Hub</a>
        </div>
        
        <div class="hero">
            <h1>SEO Bot</h1>
            <p>AI-powered SEO article generator. Rank higher in minutes.</p>
        </div>
        
        <div class="content">
            <div class="pricing-grid">
                <div class="pricing-card">
                    <h3>Starter</h3>
                    <div class="price">$29/mo</div>
                    <p>10 articles/month</p>
                    <button onclick="window.location.href='/checkout?plan=starter'">Get Started</button>
                </div>
                <div class="pricing-card featured">
                    <h3>Pro</h3>
                    <div class="price">$79/mo</div>
                    <p>50 articles/month</p>
                    <button onclick="window.location.href='/checkout?plan=pro'">Most Popular</button>
                </div>
                <div class="pricing-card">
                    <h3>Enterprise</h3>
                    <div class="price">$199/mo</div>
                    <p>Unlimited articles</p>
                    <button onclick="window.location.href='/checkout?plan=enterprise'">Contact Us</button>
                </div>
            </div>
            
            <div class="tools-links">
                <a href="/keyword">🔍 Keyword Research</a>
                <a href="/competitor">📊 Competitor Analysis</a>
            </div>
            
            <div class="generator-box">
                <h2 style="text-align: center; margin-bottom: 30px;">Try Free - Generate Article</h2>
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
                    <button type="submit" class="generate-btn">Generate Article</button>
                </form>
                <div id="result" class="result-box"></div>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('generateForm').onsubmit = async (e) => {
            e.preventDefault();
            const btn = document.querySelector('.generate-btn');
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
                resultDiv.innerHTML = `<div style="color:red;font-weight:bold;">Error: ${data.error}</div>`;
            } else {
                resultDiv.innerHTML = `
                    <h3>${data.title}</h3>
                    <div class="article">${data.content}</div>
                    <p style="color:green;font-weight:bold;margin-top:20px;">Word count: ${data.word_count}</p>
                `;
            }
            btn.textContent = 'Generate Article';
        };
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
