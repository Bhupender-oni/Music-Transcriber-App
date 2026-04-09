FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -e .

COPY . .

EXPOSE 5000
CMD ["python", "run.py", "--host", "0.0.0.0"]