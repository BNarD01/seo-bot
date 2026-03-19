# SEO Bot - Full Version with AI Generation & Stripe
import os
import json
from datetime import datetime
from openai import OpenAI
from flask import Flask, request, jsonify, render_template_string, redirect
import stripe

# Initialize
app = Flask(__name__)

# API Keys
openai_api_key = os.getenv("OPENAI_API_KEY", "")
stripe_api_key = os.getenv("STRIPE_API_KEY", "")

client = OpenAI(api_key=openai_api_key) if openai_api_key else None
stripe.api_key = stripe_api_key

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SEO Bot - AI Article Generator</title>
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
    
    <h2 style="text-align: center; margin-top: 40px;">Try Free - Generate Article</h2>
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
