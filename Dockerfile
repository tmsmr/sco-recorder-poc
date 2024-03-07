FROM python:3.12

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY recorder /recorder
WORKDIR /recorder

CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8080"]
