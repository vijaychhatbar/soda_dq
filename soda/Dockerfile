FROM python:3.8-slim-buster

WORKDIR /soda
COPY requirements.txt .
COPY configuration.yml .
COPY download_test.py .
RUN mkdir -p checks
ADD checks /checks

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "download_test.py"]
