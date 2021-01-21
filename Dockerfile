FROM python:3.7-alpine

RUN apk add --no-cache gcc make libressl-dev musl-dev libffi-dev
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY teamcounter.py ./
CMD ["python", "./teamcounter.py"]
