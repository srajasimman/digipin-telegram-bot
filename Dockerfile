# Use a minimal Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY digipin_bot.py .
COPY .env .

# Set environment variables explicitly (optional)
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "digipin_bot.py"]
