FROM python:3.7.6-buster

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY gitcounter.py ./
CMD ["python", "./gitcounter.py"]