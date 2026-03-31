from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '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')

TOOLS = [
    {"id":1,"name":"SEO Bot","category":"AI Marketing","description":"AI-powered SEO article generator. Rank higher in minutes.","price":"$29/mo","rating":4.8,"reviews":128,"link":"https://seo-bot-qrk9.onrender.com/seo-bot"},
    {"id":2,"name":"Shopify Magic","category":"AI Store Builder","description":"Shopify's official AI tool for product descriptions and marketing copy.","price":"Free (Shopify users)","rating":4.5,"reviews":256,"link":"https://www.shopify.com/magic"},
    {"id":3,"name":"DeepL Pro","category":"AI Translation","description":"Professional AI translation supporting 31 languages with high accuracy.","price":"$8.99/mo","rating":4.9,"reviews":512,"link":"https://www.deepl.com/pro"},
    {"id":4,"name":"Jasper AI","category":"AI Writing","description":"Enterprise-grade AI writing assistant for marketing teams.","price":"$49/mo","rating":4.7,"reviews":890,"link":"https://www.jasper.ai"},
    {"id":5,"name":"ChatGPT API","category":"AI Customer Service","description":"OpenAI's API for building custom AI customer service solutions.","price":"Pay per use","rating":4.8,"reviews":2100,"link":"https://openai.com/api"},
    {"id":6,"name":"Copy.ai","category":"AI Marketing","description":"AI copywriting tool for e-commerce product descriptions and ads.","price":"$36/mo","rating":4.6,"reviews":670,"link":"https://www.copy.ai"},
    {"id":7,"name":"AfterShip","category":"AI Logistics","description":"AI-powered shipment tracking and delivery notifications.","price":"$9/mo","rating":4.7,"reviews":420,"link":"https://www.aftership.com"},
    {"id":8,"name":"Stripe","category":"AI Payment","description":"Global payment platform with AI fraud detection.","price":"2.9% + 30¢","rating":4.9,"reviews":3500,"link":"https://stripe.com"},
    {"id":9,"name":"Midjourney","category":"AI Design","description":"AI image generation for high-quality marketing visuals and product photos.","price":"$10/mo","rating":4.9,"reviews":2048,"link":"https://www.midjourney.com"},
    {"id":10,"name":"ChatGPT Plus","category":"AI Customer Service","description":"OpenAI's premium plan with GPT-4 and advanced data analysis.","price":"$20/mo","rating":4.8,"reviews":5000,"link":"https://chat.openai.com"},
    {"id":11,"name":"Canva AI","category":"AI Design","description":"Online design platform with AI tools for fast marketing materials.","price":"$12.99/mo","rating":4.7,"reviews":3200,"link":"https://www.canva.com"},
    {"id":12,"name":"Surfer SEO","category":"AI Marketing","description":"AI-driven SEO optimizer for content planning and ranking analysis.","price":"$49/mo","rating":4.6,"reviews":890,"link":"https://surferseo.com"},
    {"id":13,"name":"Grammarly Business","category":"AI Writing","description":"AI writing assistant that checks grammar, style and tone for professionals.","price":"$15/user/mo","rating":4.7,"reviews":2100,"link":"https://www.grammarly.com/business"},
    {"id":14,"name":"Notion AI","category":"AI Productivity","description":"Knowledge management tool with integrated AI for content organization.","price":"$10/user/mo","rating":4.6,"reviews":1800,"link":"https://www.notion.so/product/ai"},
    {"id":15,"name":"Zapier","category":"AI Automation","description":"Automation platform connecting 5000+ apps with AI-powered workflows.","price":"$19.99/mo","rating":4.7,"reviews":2400,"link":"https://zapier.com"},
    {"id":16,"name":"HubSpot","category":"AI Marketing","description":"All-in-one marketing platform with AI-driven CRM and automation.","price":"$18/mo","rating":4.7,"reviews":3500,"link":"https://www.hubspot.com"},
]

HOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Export Hub - 16 AI Tools for Cross-Border E-Commerce</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;background:#f5f7fa;color:#333;line-height:1.6}
.header{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:60px 20px;text-align:center}
.header h1{font-size:3em;margin-bottom:10px;font-weight:700}
.header p{font-size:1.3em;opacity:.9;margin-bottom:30px}
.stats{display:flex;justify-content:center;gap:50px;margin-top:20px}
.stat-number{font-size:2.5em;font-weight:bold}
.stat-label{font-size:.9em;opacity:.8}
.promo-banner{background:#ff6b35;color:white;text-align:center;padding:12px;font-weight:bold;font-size:1.1em}
.container{max-width:1200px;margin:0 auto;padding:40px 20px}
.back-link{display:inline-block;margin-bottom:20px;color:#667eea;text-decoration:none;font-size:1em}
.back-link:hover{text-decoration:underline}
.search-box{background:white;padding:20px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,.1);margin-bottom:30px}
.search-box input{width:100%;padding:12px 18px;font-size:1em;border:2px solid #e0e0e0;border-radius:8px;outline:none}
.search-box input:focus{border-color:#667eea}
.tools-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.tool-card{background:white;border-radius:12px;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,.08);transition:transform .3s,box-shadow .3s;text-decoration:none;color:inherit;display:block}
.tool-card:hover{transform:translateY(-4px);box-shadow:0 8px 25px rgba(0,0,0,.15)}
.tool-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px}
.tool-name{font-size:1.3em;font-weight:bold;color:#333}
.tool-category{background:#f0f0f0;padding:4px 10px;border-radius:12px;font-size:.82em;color:#666;white-space:nowrap}
.tool-description{color:#666;margin-bottom:14px;font-size:.95em}
.tool-footer{display:flex;justify-content:space-between;align-items:center;padding-top:12px;border-top:1px solid #eee}
.tool-price{font-weight:bold;color:#667eea;font-size:1.05em}
.tool-rating{color:#ffa500}
.cta-section{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:60px 20px;text-align:center;margin-top:60px}
.cta-section h2{font-size:2.2em;margin-bottom:15px}
.cta-button{display:inline-block;background:white;color:#667eea;padding:14px 36px;border-radius:30px;text-decoration:none;font-weight:bold;font-size:1.1em;margin-top:20px;transition:transform .3s}
.cta-button:hover{transform:scale(1.05)}
.footer{text-align:center;padding:25px;color:#666;background:#f0f0f0}
</style>
</head>
<body>
<div class="promo-banner">🎉 Launch Special: 50% OFF with code <strong>LAUNCH50</strong></div>
<div class="header">
<h1>AI Export Hub</h1>
<p>AI-powered tools for cross-border e-commerce</p>
<div class="stats">
<div class="stat"><div class="stat-number">16</div><div class="stat-label">AI Tools</div></div>
<div class="stat"><div class="stat-number">7</div><div class="stat-label">Categories</div></div>
</div>
</div>
<div class="container">
<a href="/seo-bot" class="back-link">← Try SEO Bot Free</a>
<div class="search-box">
<input type="text" id="searchInput" placeholder="Search AI tools, e.g., SEO, translation, payment...">
</div>
<div class="tools-grid" id="toolsGrid">
TOOLS_PLACEHOLDER
</div>
</div>
<div class="cta-section">
<h2>Boost Your Export Business with AI</h2>
<p>Try our SEO Bot — generate articles in 3 minutes</p>
<a href="/seo-bot" class="cta-button">Try SEO Bot Free →</a>
</div>
<div class="footer">© 2025 AI Export Hub · Empowering sellers to go global</div>
<script>
document.getElementById('searchInput').addEventListener('input',function(e){
const q=e.target.value.toLowerCase();
document.querySelectorAll('.tool-card').forEach(c=>{
c.style.display=c.textContent.toLowerCase().includes(q)?'block':'none';
});
});
</script>
</body>
</html>"""

SEO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEO Bot - AI Article Generator</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;background:#f5f7fa;color:#333}
.header{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:40px 20px;text-align:center}
.header h1{font-size:2.5em;margin-bottom:8px}
.header p{opacity:.9;font-size:1.1em}
.container{max-width:800px;margin:40px auto;padding:0 20px}
.back-link{display:inline-block;margin-bottom:20px;color:#667eea;text-decoration:none}
.back-link:hover{text-decoration:underline}
.card{background:white;border-radius:12px;padding:30px;box-shadow:0 2px 10px rgba(0,0,0,.1)}
.input-group{display:flex;gap:10px;margin-bottom:20px}
#kw{flex:1;padding:12px 16px;font-size:1em;border:2px solid #e0e0e0;border-radius:8px;outline:none}
#kw:focus{border-color:#667eea}
button{padding:12px 24px;background:#667eea;color:white;border:none;border-radius:8px;font-size:1em;cursor:pointer;white-space:nowrap}
button:hover{background:#5a6fd8}
button:disabled{background:#aaa;cursor:not-allowed}
#status{color:#666;margin-bottom:15px;font-size:.95em}
#result{white-space:pre-wrap;line-height:1.7;color:#333;min-height:100px}
</style>
</head>
<body>
<div class="header">
<h1>SEO Bot</h1>
<p>Generate SEO-optimized articles in minutes</p>
</div>
<div class="container">
<a href="/" class="back-link">← Back to AI Export Hub</a>
<div class="card">
<div class="input-group">
<input id="kw" placeholder="Enter keyword, e.g. bluetooth headphones review">
<button onclick="gen()" id="btn">Generate</button>
</div>
<div id="status"></div>
<div id="result"></div>
</div>
</div>
<script>
async function gen(){
const k=document.getElementById('kw').value.trim();
if(!k){alert('Please enter a keyword');return;}
const btn=document.getElementById('btn');
const status=document.getElementById('status');
const result=document.getElementById('result');
btn.disabled=true;btn.textContent='Generating...';
status.textContent='Generating your article...';result.textContent='';
try{
const r=await fetch('/api/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({keyword:k})});
const d=await r.json();
if(d.article){result.textContent=d.article;status.textContent='Done!';}
else{result.textContent='Error: '+(d.error||'Unknown error');status.textContent='';}
}catch(e){result.textContent='Network error: '+e.message;status.textContent='';}
btn.disabled=false;btn.textContent='Generate';
}
document.getElementById('kw').addEventListener('keydown',e=>{if(e.key==='Enter')gen();});
</script>
</body>
</html>"""


def build_tool_card(tool):
    return f'''<a href="{tool['link']}" target="_blank" class="tool-card">
<div class="tool-header">
<div class="tool-name">{tool['name']}</div>
<span class="tool-category">{tool['category']}</span>
</div>
<div class="tool-description">{tool['description']}</div>
<div class="tool-footer">
<span class="tool-price">{tool['price']}</span>
<span class="tool-rating">⭐ {tool['rating']} ({tool['reviews']})</span>
</div>
</a>'''


@app.route('/googled01db92c3ea8ceb1.html')
def google_verify():
    return 'google-site-verification: googled01db92c3ea8ceb1.html'


@app.route('/sitemap.xml')
def sitemap():
    return '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://seo-bot-qrk9.onrender.com/</loc></url><url><loc>https://seo-bot-qrk9.onrender.com/seo-bot</loc></url></urlset>', 200, {'Content-Type': 'application/xml'}


@app.route('/')
def home():
    cards = '\n'.join(build_tool_card(t) for t in TOOLS)
    return HOME_HTML.replace('TOOLS_PLACEHOLDER', cards)


@app.route('/seo-bot')
def seo_bot():
    return SEO_HTML


@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    keyword = data.get('keyword', '')
    if not keyword:
        return jsonify({'error': 'Keyword required'}), 400
    try:
        res = requests.post('https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {OPENROUTER_API_KEY}', 'Content-Type': 'application/json'},
            json={'model': 'anthropic/claude-3.5-sonnet', 'messages': [
                {'role': 'system', 'content': 'You are an SEO expert. Write detailed, well-structured SEO articles.'},
                {'role': 'user', 'content': f'Write a comprehensive SEO article about: {keyword}'}
            ]}, timeout=60)
        result = res.json()
        return jsonify({'article': result['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
