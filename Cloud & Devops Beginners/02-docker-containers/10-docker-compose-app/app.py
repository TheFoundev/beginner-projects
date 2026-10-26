import os
import redis
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder='html', static_url_path='')
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

try:
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
except Exception as e:
    r = None

@app.route('/')
def serve_frontend():
    return send_from_directory('html', 'index.html')

@app.route('/api/count')
def get_count():
    if r:
        r.incr('visitor_count')
        count = r.get('visitor_count')
        return jsonify(count=int(count))
    return jsonify(count=-1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
