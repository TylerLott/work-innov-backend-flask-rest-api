# Specify Base Image
FROM python:3.8.10-slim

# Set working dir
WORKDIR /app

# Install Dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

# Default Commands
CMD ["flask", "run"]