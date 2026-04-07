# syntax=docker/dockerfile:1
# ARC runner with Python 3 + kubectl for cluster operations.
# Extends the official GitHub Actions runner image.
FROM ghcr.io/actions/actions-runner:latest

USER root

ARG KUBECTL_VERSION=v1.35.0
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv curl \
    && curl -fsSL -o /usr/local/bin/kubectl \
        "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" \
    && chmod +x /usr/local/bin/kubectl \
    && apt-get purge -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir --break-system-packages -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

USER runner
