FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install --no-cache-dir . uv

COPY . .

EXPOSE 6969

CMD ["uv", "run", "calculator.py", "--mode", "streamable-http"]
