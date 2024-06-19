FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY geturls.py .

RUN groupadd -r tooluser && useradd -r -g tooluser tooluser

RUN chown -R tooluser:tooluser /app
RUN chmod -R 755 /app

USER tooluser

ENTRYPOINT ["python", "geturls.py"]
CMD ["-h"] 
