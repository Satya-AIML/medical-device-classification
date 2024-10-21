FROM python:3.12.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install necessary system packages and AWS CLI
RUN apt update -y && apt install -y awscli \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade accelerate
RUN pip uninstall -y transformers accelerate
RUN pip install --no-cache-dir transformers accelerate

# Copy the rest of the application code
COPY . .

# Start the application
CMD ["python3", "app.py"]




