# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

RUN pip install --upgrade pip

# Install dependencies
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 15000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=15000", "--reload"]

