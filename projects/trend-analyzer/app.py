from flask import Flask, render_template, request, jsonify
from analyzer import TrendAnalyzer
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json.get('data', [])
        labels = request.json.get('labels', [])
        method = request.json.get('method', 'standard')
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        analyzer = TrendAnalyzer(data, labels=labels)
        results = analyzer.get_analysis_results(method=method)
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
