FROM python:3.7-alpine

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY *.py ./
ENV PYTHONUNBUFFERED=1
CMD ["./piocheck-codecoverage.py"]