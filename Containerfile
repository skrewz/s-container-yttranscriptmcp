FROM python:3.13-slim AS builder

WORKDIR /build

RUN pip install --no-cache-dir --upgrade pip

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target /build/deps

FROM python:3.13-slim

WORKDIR /app

RUN groupadd -r mcp && useradd -r -g mcp mcp

COPY --from=builder /build/deps /usr/local/lib/python3.13/site-packages

COPY src/mcp_server.py .
COPY src/requirements.txt .

RUN chown -R mcp:mcp /app

USER mcp

ENV PYTHONUNBUFFERED=1

EXPOSE 9042

CMD ["python", "mcp_server.py"]
