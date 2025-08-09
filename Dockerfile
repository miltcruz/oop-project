FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ODBC runtime + MS driver (Debian 12 / bookworm)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg ca-certificates apt-transport-https unixodbc \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/ms-packages.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/ms-packages.gpg arch=amd64,arm64] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
# Defaults; override via env / compose
ENV DB_PROVIDER=sqlite SQLITE_DB_PATH=/app/data/oop.db
CMD ["uvicorn","api.main:app","--host","0.0.0.0","--port","8000"]