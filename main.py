from flask import Flask
import os

app = Flask(__name__)

@app.route('/googled01db92c3ea8ceb1.html')
def google_verify():
    return 'google-site-verification: googled01db92c3ea8ceb1.html'

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="2q_7K4_mtroLrVF8FsZELgR02XEjNaRGgPfbm5sJNJY" />
    <title>AI SEO Tool | AI Export Hub</title>
</head>
<body>
    <h1>AI Export Hub - 16 AI Tools</h1>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
