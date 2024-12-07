FROM python:3.13-slim

COPY . .

RUN apt-get update && \
    apt-get install --no-install-recommends -y && \
    pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"]