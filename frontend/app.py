import requests
import time
import re
import datetime
import threading
from flask import Flask, render_template, Response, send_from_directory
import os
import sys

url = "localhost"
if len(sys.argv) > 1 and sys.argv[1] == "docker":
    url = "backend"

app = Flask(__name__)

@app.route("/save")
def save_video():
    
    try:
        res = requests.get(f"http://backend:8002/getclip")
        status = "ERROR GENERATING VIDEO"
        if res.status_code == 200:
            bts = res.content
            print(len(bts))
            if len(bts) != 0:
                dt = datetime.datetime.now()
                fname = f"{dt.year}_{dt.month}_{dt.day}_{dt.hour}_{dt.minute}_{dt.second}_{dt.microsecond}"
                with open(f"videos/{fname}.mp4", "xb") as f:
                    f.write(bts)
                f.close()
                os.system(f"ffmpeg -i videos/{fname}.mp4 -vcodec h264 -acodec aac videos/converted_{fname}.mp4")
                os.remove(f"videos/{fname}.mp4")
                status = "CLIP SAVED"
                return render_template('saved.html', video=f"converted_{fname}.mp4", status=status)
    except:
        print(f'err: {url}')
    return f'errror happened'
    

@app.route('/videos/<path:filename>')
def serve_video(filename):
    # Serve the video file from the /videos directory
    return send_from_directory('videos', filename)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)