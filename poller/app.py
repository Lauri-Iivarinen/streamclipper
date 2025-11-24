import requests
import json
import time
import sys
import re
from copy import deepcopy

url = "localhost"
if len(sys.argv) > 1 and sys.argv[1] == "docker":
    url = "backend"

videos: dict[str: bytearray] = {}
video_order = []
polling = False
video_index = 0

def get_stream_address():
    res = requests.get(f"https://g0.ipcamlive.com/player/getcamerastreamstate.php?_=1763815864005&token=50sZH1wbvMhgjSagulqZwIsvvv5ubW5h0NISgYm%2BzQ0%3D&alias=lastenrinne&targetdomain=g0.ipcamlive.com&viewerid=1356447989&bufferingpercent=0")
    body = res.json()
    server = re.findall("[0-9]+", body["details"]["address"])[0]
    id = body["details"]["streamid"]
    return server, id

#print(get_stream_address())
def generate(a):
    for chunk in a:
        yield chunk

def poll_webcam():
    global videos
    global video_order
    global polling
    print('Started polling')
    id = "16cnulvvhi8x9ltwj"
    server = "22"
    count = 0
    server, id = get_stream_address()


    while True:
        print(len(videos.keys()))
        try:
            count = count + 1
            res = requests.get(f"https://s{server}.ipcamlive.com/streams/{id}/stream.m3u8")
            if res.status_code != 200:
                print("Error while polling stream endpoint")
                server, id = get_stream_address()
            body = res.text
            streams = re.findall("stream_[0-9]*_.*\.ts", body)[1:-1]
            for s in streams:
                if s not in videos:
                    res = requests.get(f"https://s{server}.ipcamlive.com/streams/{id}/{s}")
                    if res.status_code == 200:
                        #print(f"{s} - {len(video_order)}:{len(videos.keys())}")
                        videos[s] = res.content
                        video_order.append(s)
                        if len(video_order) > 20:
                            videos.pop(video_order[0])
                            video_order = video_order[1:]
                    else:
                        print("error polling segment of video")


            video_copy = deepcopy(videos)
            vids = []
            vd = deepcopy(video_order)

            vd.reverse()
            if len(vd) > 15:
                vd = vd[0:15]
            vd.reverse()

            for v in vd:
                vids.append(video_copy[v])

            try:
                response = requests.post(f'http://{url}:8002/insertbuffer', data=generate(vids), headers={'content-type': 'application/octet-stream'})
            except:
                print("Err sending")
        except:
            print('some error occurred')
        time.sleep(4) # sleeping 5 sec would poll only 120 times an hour, we can poll a bit more to keep it consistent

if __name__ == '__main__':
    time.sleep(10) # Give backend some time to spin up
    poll_webcam()

