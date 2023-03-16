FROM ghcr.io/nais/docker-github-runner:26
ENV RUNNER_LABELS gitcounter

USER root
RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install --upgrade pip

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY gitcounter.py /opt/
RUN chmod a+rx /opt/gitcounter.py

USER runner
WORKDIR /opt/runner
