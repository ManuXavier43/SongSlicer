# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

RUN mkdir -p /app/src/deezer/music_in

# Install system dependencies for tkinter
RUN apt-get update && apt-get install -y \
    tk \
    ffmpeg \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install pydub

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose Flask's default port
EXPOSE 5000

# Command to run the main script
CMD ["python", "src/main.py"]
