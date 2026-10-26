FROM python:3.11-slim

LABEL org.opencontainers.image.title="madlibs-generator" \
      org.opencontainers.image.description="Mad Libs story generator with multiple templates" \
      org.opencontainers.image.version="1.0.0"

WORKDIR /app

COPY app.py .
COPY tests/ tests/

ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python app.py --help || exit 1

ENTRYPOINT ["python", "app.py"]
CMD ["--help"]
