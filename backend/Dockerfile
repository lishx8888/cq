FROM python:3.12-alpine AS builder

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-alpine

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY backend/ .

RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]