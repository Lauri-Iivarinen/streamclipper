import requests
import time
import re
import datetime
import threading
from flask import Flask, render_template, Response
import os
from copy import deepcopy

#app = Flask(__name__)

videos = {}
video_order = []
polling = False
video_index = 0

def get_stream_address():
    res = requests.get(f"https://g0.ipcamlive.com/player/getcamerastreamstate.php?_=1734719940015&token=w1o6ryGjh%2BL1bBCqddHrQ3%2FPHPjS0x3IWQ2zhUx7X8E%3D&alias=streetkamera&targetdomain=g0.ipcamlive.com")
    body = res.json()
    server = re.findall("[0-9]+", body["details"]["address"])[0]
    id = body["details"]["streamid"]
    return server, id

def poll_webcam():
    global videos
    global video_order
    global polling

    id = "16cnulvvhi8x9ltwj"
    server = "22"
    count = 0
    server, id = get_stream_address()


    while True:
        count = count + 1
        res = requests.get(f"https://s{server}.ipcamlive.com/streams/{id}/stream.m3u8")
        if res.status_code != 200:
            print("Error while polling endpoint")
            server, id = get_stream_address()
        body = res.text
        streams = re.findall("stream_[0-9]*_.*\.ts", body)[1:-1]
        for s in streams:
            if s not in videos:
                res = requests.get(f"https://s{server}.ipcamlive.com/streams/{id}/{s}")
                if res.status_code == 200:
                    print(f"{s} - {len(video_order)}:{len(videos.keys())}")
                    videos[s] = res.content
                    video_order.append(s)
                    if len(video_order) > 20:
                        videos.pop(video_order[0])
                        video_order = video_order[1:]
                else:
                    print("error")
        time.sleep(1)


app = Flask(__name__)
threading.Thread(target = poll_webcam).start()

def generate(a):
    for chunk in a:
        yield chunk

@app.route("/smoke")
def get_smoke():
    return "ok"

@app.route("/getrecent")
def get_recent():
    global videos
    global video_order

    video_copy = deepcopy(videos)
    vids = []
    vd = deepcopy(video_order)

    vd.reverse()
    if len(vd) > 15:
        vd = vd[0:15]
    vd.reverse()

    for v in vd:
        vids.append(video_copy[v])

    return Response(generate(vids), content_type='application/octet-stream')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)