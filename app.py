from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Flask DevOps Project is running!'
    })

@app.route('/api/info')
def info():
    return jsonify({
        'project': 'DevOps Group Project',
        'version': '1.0',
        'team': 'Dream Team'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

