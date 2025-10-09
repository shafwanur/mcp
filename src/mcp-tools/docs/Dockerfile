FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install --no-cache-dir . uv

COPY . .

EXPOSE 3333

CMD ["uv", "run", "docs.py", "--mode", "streamable-http"]
