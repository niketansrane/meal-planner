FROM python:3.12-slim

# Create a working directory
WORKDIR /code

# Copy requirements file
COPY requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --ignore-installed -r /code/requirements.txt

# Copy application code
COPY app/ /code/app

# Copy static files
COPY static/ /code/static/

# Expose port 80
EXPOSE 80

# Use uvicorn to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
