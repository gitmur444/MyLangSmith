FROM mcr.microsoft.com/devcontainers/python:0-3.10

# Install Python dependencies
COPY requirements.txt /tmp/pip-tmp/
RUN pip install --no-cache-dir -r /tmp/pip-tmp/requirements.txt
RUN pip install --no-cache-dir openai

# Copy all sources into container workspace (works for Codespaces and local Docker)
COPY . /workspace
WORKDIR /workspace
ENV PYTHONPATH=/workspace

