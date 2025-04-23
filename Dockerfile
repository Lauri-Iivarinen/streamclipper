# Stage 1: Build dependencies
FROM ubuntu:latest AS dependencies

WORKDIR /app

# Install dependencies
RUN apt update && apt install -y python3 python3-pip ffmpeg

# Copy and install Python requirements
COPY requirements.txt ../requirements.txt
RUN pip install --break-system-packages -r ../requirements.txt


# Stage 2: Copy app-specific code
FROM dependencies AS app

WORKDIR /app
COPY . .

# Run the application
CMD ["python3", "app.py" , "docker"]
