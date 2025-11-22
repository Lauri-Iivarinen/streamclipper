# Backend #
- keeps updated video rewady to be served
- decides url for the poller
- serves video to front

# Front #
- Fetch video from backend upon request
- format it using ffmpeg
- Allows downloading of said video

# Poller #
- Constantly fetches new video feed from webcam url
- generates video from bytes (There was some issues pushing this stuff to backend raw, which would be more optimal)
- pushes updated video to backend

# TODO #
- Error handling
- Automatic new url fetching

# run code #
run this on root to launch docker container
```
docker compose up -d
```