from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# API Keys
OPENROUTER_API_KEY = "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"
SERPAPI_KEY = "f93zltAES7x352JZV9rldICew"

# Google verification
@app.route('/googled01db92c3ea8ceb1.html')
def google_verify():
    return 'google-site-verification: googled01db92c3ea8ceb1.html'

# Sitemap for SEO
@app.route('/sitemap.xml')
def sitemap():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://seo-bot-qrk9.onrender.com/</loc>
    <lastmod>2026-03-30</lastmod>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://seo-bot-qrk9.onrender.com/blog/ai-seo-tools</loc>
    <lastmod>2026-03-30</lastmod>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://seo-bot-qrk9.onrender.com/blog/ecommerce-seo</loc>
    <lastmod>2026-03-30</lastmod>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://seo-bot-qrk9.onrender.com/blog/content-marketing</loc>
    <lastmod>2026-03-30</lastmod>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://seo-bot-qrk9.onrender.com/seo-bot</loc>
    <lastmod>2026-03-30</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>''', 200, {'Content-Type': 'application/xml'}

# Home page with SEO
@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="2q_7K4_mtroLrVF8FsZELgR02XEjNaRGgPfbm5sJNJY" />
    <title>AI SEO Tool - Write SEO Articles in 3 Minutes | AI Export Hub</title>
    <meta name="description" content="Write SEO-optimized articles in 3 minutes with AI. 16 AI tools for ecommerce. Free trial. 50% off with LAUNCH50.">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow-lg">
        <div class="container mx-auto px-6 py-4">
            <div class="flex justify-between items-center">
                <h1 class="text-2xl font-bold text-blue-600">AI Export Hub</h1>
                <div class="space-x-4">
                    <a href="/" class="text-gray-700 hover:text-blue-600">Home</a>
                    <a href="/blog/ai-seo-tools" class="text-gray-700 hover:text-blue-600">Blog</a>
                    <a href="/seo-bot" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Try SEO Bot</a>
                </div>
            </div>
        </div>
    </nav>
    
    <section class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div class="container mx-auto px-6 text-center">
            <h1 class="text-5xl font-bold mb-6">AI SEO Tool - Write Articles in 3 Minutes</h1>
            <p class="text-xl mb-8">16 AI tools for e-commerce. SEO-optimized content that ranks.</p>
            <div class="space-x-4">
                <a href="/seo-bot" class="bg-white text-blue-600 px-8 py-3 rounded-full font-bold hover:bg-gray-100">Start Free Trial</a>
                <span class="bg-yellow-400 text-black px-4 py-2 rounded-full font-bold">50% OFF: LAUNCH50</s
pan>
            </div>
        </div>
    </section>
    
    <section class="py-16">
        <div class="container mx-auto px-6">
            <h2 class="text-3xl font-bold text-center mb-12">Latest Blog Posts</h2>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="bg-white p-6 rounded-lg shadow">
                    <h3 class="text-lg font-bold mb-2">10 Best AI SEO Tools 2026</h3>
                    <a href="/blog/ai-seo-tools" class="text-blue-600 hover:underline">Read more →</a>
                </div>
<div class="bg-white p-6 rounded-lg shadow">
                    <h3 class="text-lg font-bold mb-2">Ecommerce SEO Guide</h3>
                    <a href="/blog/ecommerce-seo" class="text-blue-600 hover:underline">Read more →</a>
                </div>
                <div class="bg-white p-6 rounded-lg shadow">
                    <h3 class="text-lg font-bold mb-2">Content Marketing with AI</h3>
                    <a href="/blog/content-marketing" class="text-blue-600 hover:underline">Read more →</a>
                </div>
            </div>
        </div>
    </section>
</body>
</html>'''

# Blog pages
@app.route('/blog/ai-seo-tools')
def blog_ai_seo():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>10 Best AI SEO Tools to Rank #1 on Google in 2026 | AI Export Hub</title>
    <meta name="description" content="Discover the top 10 AI SEO tools that can help you rank #1 on Google. Includes AI Export Hub, Jasper, Copy.ai and more.">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <article class="container mx-auto px-6 py-12 max-w-4xl">
        <h1 class="text-4xl font-bold mb-6">10 Best AI SEO Tools to Rank #1 on Google in 2026</h1>
        <div class="prose lg:prose-xl">
            <p class="text-lg mb-6">SEO is changing fast. AI tools now write articles, optimize keywords, and boost rankings automatically.</p>
            <h2 class="text-2xl font-bold mt-8 mb-4">Top 10 AI SEO Tools</h2>
            <div class="bg-blue-50 p-6 rounded-lg mb-6">
                <h3 class="text-xl font-bold mb-2">1. AI Export Hub - Best for E-commerce</h3>
                <p>Writes SEO articles in 3 minutes. 16 AI tools included. Free trial available.</p>
                <a href="/" class="text-blue-600 hover:underline mt-4 inline-block">Try AI Export Hub Free →</a>
            </div>
        </div>
    </article>
</body>
</html>'''

@app.route('/blog/ecommerce-seo')
def blog_ecommerce():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecommerce SEO: How to Drive Traffic to Your Online Store | AI Export Hub</title>
    <meta name="description" content="Learn proven ecommerce SEO strategies to drive free traffic to your online store.">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <article class="container mx-auto px-6 py-12 max-w-4xl">
        <h1 class="text-4xl font-bold mb-6">Ecommerce SEO: How to Drive Traffic to Your Online Store</h1>
        <p class="text-lg mb-6">Running an online store? SEO is your best friend for generating free, targeted traffic.</p>
        <a href="/" class="bg-blue-600 text-white px-6 py-2 rounded mt-4 inline-block">Try Free</a>
    </article>
</body>
</html>'''

@app.route('/blog/content-marketing')
def blog_content():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Content Marketing Strategy: Scale 10x with AI | AI Export Hub</title>
    <meta name="description" content="Learn how to scale your content marketing 10x with AI tools.">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <article class="container mx-auto px-6 py-12 max-w-4xl">
        <h1 class="text-4xl font-bold mb-6">Content Marketing Strategy: Scale 10x with AI</h1>
        <p class="text-lg mb-6">Struggling to create enough content? AI can help you scale 10x.</p>
        <div class="bg-yellow-50 p-6 rounded-lg mt-6">
            <p class="font-bold">Try AI Export Hub free! Use code LAUNCH50 for 50% off.</p>
            <a href="/" class="bg-blue-600 text-white px-6 py-2 rounded mt-4 inline-block">Start Free Trial</a>
        </div>
    </article>
</body>
</html>'''

# SEO Bot tool page
@app.route('/seo-bot')
def seo_bot():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Bot - AI Article Writer | AI Export Hub</title>
    <meta name="description" content="Write SEO-optimized articles in 3 minutes with AI. Free trial available.">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-6 py-12">
        <h1 class="text-4xl font-bold text-center mb-8">SEO Bot</h1>
        <p class="text-center text-gray-600 mb-8">Write SEO-optimized articles in 3 minutes</p>
        <div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
            <p class="text-center">AI-powered content generation coming soon!</p>
            <p class="text-center mt-4">Use code <strong>LAUNCH50</strong> for 50% off</p>
        </div>
    </div>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

