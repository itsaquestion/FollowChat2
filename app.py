from flask import Flask, jsonify, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_files')
def list_files():
    files = os.listdir('data/scripts')
    txt_files = [f for f in files if f.endswith('.txt')]
    return jsonify(txt_files)

@app.route('/read_file', methods=['POST'])
def read_file():
    file_name = request.json['file_name']
    with open(f"data/scripts/{file_name}", 'r', encoding='utf-8') as f:
        content = f.read()
    return jsonify(content)

if __name__ == '__main__':
    app.run(debug=True)
