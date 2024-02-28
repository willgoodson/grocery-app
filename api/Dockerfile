# Base image
FROM python:3.11-slim

# Work directory
WORKDIR /app

# Copy requirements file
COPY ../requirements.txt ./

# Install requirements
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Entry point
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
