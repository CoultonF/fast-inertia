FROM python:3.11-slim

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -ms /bin/bash vscode

# Install Poetry
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \ 
    && poetry config virtualenvs.in-project true

# Set ownership for poetry installation
RUN chown -R vscode:vscode /opt/poetry

USER vscode

# Set working directory
WORKDIR /workspace

# We don't copy any project files here - they will be mounted by DevContainer