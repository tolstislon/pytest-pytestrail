from flask import Flask, request, redirect, jsonify, logging
import re

MAX_RUN_ID = 1000

app = Flask(__name__)


@app.route('/api/v2/get_tests/<int:run_id>')
def get_tests(run_id):
    if 0 < run_id <= MAX_RUN_ID:
        return jsonify([{'case_id': i, 'title': f'test_{i}'} for i in range(1, run_id + 1)]), 200
    else:
        return jsonify({'error': 'Field :run_id is not a valid test run.'}), 400


@app.route('/api/v2/add_result_for_case/<int:run_id>/<int:case_id>', methods=['POST', 'GET'])
def add_result_for_case(run_id, case_id):
    if 0 < run_id <= MAX_RUN_ID and 0 < case_id <= MAX_RUN_ID:
        return jsonify([
            {'assignedto_id': 1, 'g': '...'}, {'assignedto_id': 2, 'g': '...'}, {'assignedto_id': 3, 'g': '...'}
        ])
    else:
        return jsonify({'error': 'Invalid or unknown test'}), 400


@app.route('/')
def index():
    return 'pytest_pytestrail test server'


@app.route('/index.php', methods=['POST', 'GET'])
def index_php():
    if request.method == 'POST':
        print(logging.request.json)
    q = re.sub(r'/index\.php\?', '', request.url)
    h = re.sub('%2F', '/', q)
    return redirect(h)


app.run(debug=True)
