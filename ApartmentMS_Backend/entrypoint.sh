#!/bin/bash

# .env dosyasını yükle
if [ -f .env ]; then
  echo "Loading environment variables from .env file..."
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found. Ensure it is present in the root directory."
  exit 1
fi

# PostgreSQL servisinin çalıştığını kontrol et
postgres_host=$DB_HOST
postgres_port=$DB_PORT

echo "Postgres Host: $postgres_host"
echo "Postgres Port: $postgres_port"

# PostgreSQL bağlantısını kontrol et
while ! pg_isready -h "$postgres_host" -p "$postgres_port" >/dev/null 2>&1; do
  echo "PostgreSQL is not operational yet, waiting... ($postgres_host:$postgres_port)"
  sleep 5
done

echo "PostgreSQL is operational! Proceeding..."

# Gerekli Python paketlerini yükle
echo "Installing required Python packages..."
pip install -r requirements.txt

# Flask uygulamasını başlat
echo "Starting Flask application..."
exec python app.py
