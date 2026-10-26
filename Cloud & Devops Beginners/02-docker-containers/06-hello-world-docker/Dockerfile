FROM python:3.11-slim

LABEL org.opencontainers.image.title="docker-hello-world-greeting" \
      org.opencontainers.image.description="A multilingual greeting application running in Docker" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.author="Cloud & DevOps Beginners" \
      org.opencontainers.image.source="https://github.com/example/docker-hello-world"

WORKDIR /app

# Set default environment variables
ENV GREETING_NAME=Docker \
    GREETING_LANG=english \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install app dependencies (none needed for stdlib)
# Copy source code
COPY app.py .

# Run as non-root user for security
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check — verify the app runs
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python app.py --name healthcheck || exit 1

ENTRYPOINT ["python", "app.py"]
CMD ["--help"]
