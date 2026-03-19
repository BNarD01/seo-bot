# SEO Bot - Simple Version
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SEO Bot - AI Article Generator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .pricing { display: flex; gap: 20px; margin: 30px 0; }
        .plan { flex: 1; padding: 20px; border: 2px solid #ddd; border-radius: 10px; text-align: center; }
        .plan.featured { border-color: #007bff; }
        .price { font-size: 2em; color: #007bff; }
        button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>SEO Bot</h1>
    <p>AI-powered SEO article generator. Coming soon!</p>
    
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
    
    <p>Website launching soon. Contact us for early access!</p>
    <button>Join Waitlist</button>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
