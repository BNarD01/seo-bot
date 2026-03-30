from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = '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'

@app.route('/googled01db92c3ea8ceb1.html')
def google_verify():
    return 'google-site-verification: googled01db92c3ea8ceb1.html'

@app.route('/sitemap.xml')
def sitemap():
    return '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://seo-bot-qrk9.onrender.com/</loc></url></urlset>', 200, {'Content-Type': 'application/xml'}

@app.route('/')
def home():
    return '<h1>AI Export Hub - 16 AI Tools</h1><p>SEO Bot, Product Writer, Keyword Research</p><a href="/seo-bot">Try SEO Bot</a>'

@app.route('/seo-bot')
def seo_bot():
    return '<h1>SEO Bot</h1><input id="kw" placeholder="keyword"><button onclick="gen()">Generate</button><div id="r"></div><script>async function gen(){const k=document.getElementById("kw").value;const r=await fetch("/api/generate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({keyword:k})});const d=await r.json();document.getElementById("r").innerText=d.article||d.error;}</script>'

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
                {'role': 'system', 'content': 'You are an SEO expert.'},
                {'role': 'user', 'content': f'Write SEO article about: {keyword}'}
            ]}, timeout=60)
        result = res.json()
        return jsonify({'article': result['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
