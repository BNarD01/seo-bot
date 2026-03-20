# Keyword Research Feature for SEO Bot
import os
from openai import OpenAI
from flask import Blueprint, request, jsonify, render_template_string

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

keyword_bp = Blueprint('keyword', __name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Keyword Research - SEO Bot</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #333; text-align: center; }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
        button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background: #0056b3; }
        .result { margin-top: 30px; padding: 20px; background: white; border-radius: 5px; border-left: 4px solid #007bff; }
        .keyword-item { padding: 10px; margin: 5px 0; background: #f8f9fa; border-radius: 5px; }
        .score { display: inline-block; padding: 5px 10px; border-radius: 20px; font-weight: bold; }
        .score-high { background: #28a745; color: white; }
        .score-medium { background: #ffc107; color: black; }
        .score-low { background: #dc3545; color: white; }
    </style>
</head>
<body>
    <h1>Keyword Research Tool</h1>
    <p style="text-align: center; color: #666;">Analyze keywords for SEO potential</p>
    
    <form id="researchForm">
        <div class="form-group">
            <label>Enter Keyword:</label>
            <input type="text" id="keyword" placeholder="e.g., coffee maker, digital marketing" required>
        </div>
        <button type="submit">Analyze Keyword</button>
    </form>
    
    <div id="result" style="display:none;"></div>
    
    <script>
        document.getElementById('researchForm').onsubmit = async (e) => {
            e.preventDefault();
            const btn = document.querySelector('button');
            btn.textContent = 'Analyzing...';
            
            const res = await fetch('/keyword/research', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({keyword: document.getElementById('keyword').value})
            });
            
            const data = await res.json();
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            
            if (data.error) {
                resultDiv.innerHTML = `<div style="color: red;">Error: ${data.error}</div>`;
            } else {
                let html = `<h2>Results for "${data.keyword}"</h2>`;
                html += `<div class="keyword-item"><strong>Search Volume:</strong> ${data.search_volume}</div>`;
                html += `<div class="keyword-item"><strong>Difficulty:</strong> <span class="score score-${data.difficulty_level}">${data.difficulty}/100</span></div>`;
                html += `<div class="keyword-item"><strong>Competition:</strong> ${data.competition}</div>`;
                html += `<div class="keyword-item"><strong>Opportunity Score:</strong> <span class="score score-${data.opportunity_level}">${data.opportunity}/100</span></div>`;
                
                html += `<h3>Related Keywords:</h3>`;
                data.related_keywords.forEach(kw => {
                    html += `<div class="keyword-item">${kw}</div>`;
                });
                
                html += `<h3>Recommendations:</h3>`;
                html += `<div class="keyword-item">${data.recommendations}</div>`;
                
                resultDiv.innerHTML = html;
            }
            btn.textContent = 'Analyze Keyword';
        };
    </script>
</body>
</html>
"""

@keyword_bp.route('/')
def keyword_page():
    return render_template_string(HTML_TEMPLATE)

@keyword_bp.route('/research', methods=['POST'])
def research_keyword():
    data = request.json
    keyword = data.get('keyword', '').strip()
    
    if not keyword:
        return jsonify({"error": "Keyword required"}), 400
    
    try:
        # Use OpenAI to analyze keyword
        prompt = f"""Analyze the SEO keyword "{keyword}" and provide:

1. Estimated monthly search volume (Low/Medium/High)
2. Keyword difficulty score (0-100)
3. Competition level (Low/Medium/High)
4. Opportunity score (0-100, higher = better)
5. 5 related long-tail keywords
6. Brief recommendation

Format as JSON:
{{
    "search_volume": "Medium",
    "difficulty": 45,
    "competition": "Medium",
    "opportunity": 65,
    "related_keywords": ["keyword 1", "keyword 2", ...],
    "recommendations": "Go for it! This keyword has good volume and manageable competition."
}}"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        # Parse the response
        import json as json_lib
        result_text = response.choices[0].message.content
        
        # Extract JSON from response
        try:
            result = json_lib.loads(result_text)
        except:
            # If not valid JSON, create structured response
            result = {
                "search_volume": "Medium",
                "difficulty": 50,
                "competition": "Medium", 
                "opportunity": 60,
                "related_keywords": [f"best {keyword}", f"top {keyword}", f"{keyword} guide", f"{keyword} tutorial", f"{keyword} 2024"],
                "recommendations": f"Target this keyword with high-quality content. Focus on user intent and provide comprehensive coverage."
            }
        
        # Add difficulty level for styling
        difficulty = result.get('difficulty', 50)
        if difficulty < 30:
            result['difficulty_level'] = 'low'
        elif difficulty < 70:
            result['difficulty_level'] = 'medium'
        else:
            result['difficulty_level'] = 'high'
        
        # Add opportunity level for styling
        opportunity = result.get('opportunity', 60)
        if opportunity >= 70:
            result['opportunity_level'] = 'high'
        elif opportunity >= 40:
            result['opportunity_level'] = 'medium'
        else:
            result['opportunity_level'] = 'low'
        
        result['keyword'] = keyword
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
