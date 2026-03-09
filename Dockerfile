FROM python:3.11-slim

# install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# working directory
WORKDIR /app

# copy requirements
COPY requirements.txt .

# install python libs
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# run script with virtual display
CMD ["python", "main.py"]