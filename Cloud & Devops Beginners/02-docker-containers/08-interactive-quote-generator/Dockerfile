FROM python:3.11-slim

LABEL org.opencontainers.image.title="docker-quote-generator" \
      org.opencontainers.image.description="A motivational quote generator with category filtering" \
      org.opencontainers.image.version="1.0.0"

WORKDIR /app

COPY app.py quotes.json ./

ENV PYTHONUNBUFFERED=1 \
    QUOTE_FILE=/app/quotes.json

RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["python", "app.py"]
CMD ["--help"]
