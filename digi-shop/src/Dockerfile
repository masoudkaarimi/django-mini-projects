FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV DJANGO_SETTINGS_MODULE=core.settings.production

# Set work directory
WORKDIR /src

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /src/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy package.json and install NPM dependencies
COPY package.json package-lock.json* /src/
RUN npm install

# Copy project files
COPY . /src/

# Setup Django before building
RUN python manage.py collectstatic --noinput || echo "Skipping initial collectstatic"
RUN python manage.py migrate --noinput || echo "Skipping initial migrate"

# Build frontend assets
RUN npm run build

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
