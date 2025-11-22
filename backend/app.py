import requests
from flask import Flask, render_template, Response, request
import json
from copy import deepcopy

app = Flask(__name__)

buffer = []
url = 'talma.fi'
video = []
order: list[str] = []

@app.route('/')
def index():
    return ':)'

@app.route('/insertbuffer', methods=['POST'])
def insert_buffer():
    global video
    video = request.data
    return '200'


@app.route("/getclip")
def get_recent():
    global video
    return Response(video, content_type='application/octet-stream')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)