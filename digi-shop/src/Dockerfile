FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV DEBIAN_FRONTEND=noninteractive
ENV DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

EXPOSE 8000

# Set work directory
WORKDIR /usr/src

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
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy package.json and install NPM dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy project files
COPY . .

# Build frontend assets
RUN npm run build

# Setup Django before building
#RUN python manage.py collectstatic --noinput || echo "Skipping initial collectstatic"
#RUN python manage.py migrate --noinput || echo "Skipping initial migrate"

# Copy entrypoint script
COPY entrypoint.sh /usr/src/
RUN chmod +x /usr/src/entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/usr/src/entrypoint.sh"]

# Run gunicorn
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
# or
#CMD ["gunicorn", "-c", "core/gunicorn.py", "core.wsgi:application"]
