FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python ./wait_for_client.py && python ./app.py generate_key && uvicorn app:app --host 0.0.0.0 --port 8000
