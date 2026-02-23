FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the app, including templates
COPY . .

# Expose the port Heroku expects
EXPOSE 5000

# Start the app with Gunicorn
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:$PORT --workers=1 --timeout=120"]