# Dockerfile for VPN Management Service

FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy source code
COPY src/ ./src/
COPY main.py .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
