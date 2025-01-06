#Use Python 3.9 for Spleeter to work
FROM python:3.9-slim

#App root folder for docker container
WORKDIR /app
#Where songs are saved/local songs found
RUN mkdir -p /app/src/splits/music_in

#Dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#Install other requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy app files
COPY . .

#Set PYTHONPATH to include /app and src folder
#ENV PYTHONPATH=/app
ENV PYTHONPATH=/app/src:/app

EXPOSE 8080

# Run main
CMD ["python", "src/main.py"]

#Testing
# CMD ["pytest", "src/tests/test_routes.py", "--tb=short"]