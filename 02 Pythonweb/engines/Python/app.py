from flask import Flask, render_template, jsonify, request
import os
from stats import init_db, fetch_all_records, insert_record, get_age_statistics

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../templates'))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../static'))

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Inicializamos la base de datos al arrancar
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/records', methods=['GET'])
def get_records():
    # El servidor solo delega la llamada
    records = fetch_all_records()
    return jsonify(records)

@app.route('/api/records', methods=['POST'])
def add_record():
    data = request.get_json()
    new_id = insert_record(data)
    return jsonify({'success': True, 'id': new_id})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    result = get_age_statistics()
    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)