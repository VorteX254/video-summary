# Pinned: the pinned torch/whisper versions have no wheels for newer Pythons
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# yt-dlp needs a JavaScript runtime (Deno) to download from YouTube
COPY --from=denoland/deno:bin /deno /usr/local/bin/deno

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p dump models static templates

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]