# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port that Uvicorn will run on (FastAPI's default)
EXPOSE 8000

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
