# encoding: utf-8

import os, sys, time
import common
from flask import Flask, request, send_from_directory, jsonify

"""
usage: path
"""

WORK_DIR = os.path.abspath(os.path.curdir)
if len(sys.argv) > 1:
    WORK_DIR = os.path.abspath(sys.argv[1])


app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/time')
def gettime():
    return str(time.time())

@app.route('/walk')
def walk():
    data = common.walk(WORK_DIR)
    return jsonify(data)

@app.route('/download/<path:path>')
def download(path):
    return send_from_directory(WORK_DIR, path)

@app.route('/upload/<path:path>', methods=['POST'])
def upload(path):
    f = request.files['file']
    path = os.path.abspath(os.path.join(WORK_DIR, path))
    assert WORK_DIR in path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    f.save(path)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2333, debug=False)
