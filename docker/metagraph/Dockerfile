FROM python:3.11.10-slim

# Install dependencies
RUN apt-get -y update && \
    apt-get install --no-install-recommends -y \
    git \
    cron \
    build-essential \
    rustc \
    cargo && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application files
COPY src src
COPY pyproject.toml pyproject.toml

# Install Python dependencies
RUN pip install .

# Copy cron job and set permissions
COPY ./src/consensus/metagraph/metagraphcron /etc/cron.d/metagraphcron
RUN chmod 0644 /etc/cron.d/metagraphcron
RUN crontab /etc/cron.d/metagraphcron

# Add entrypoint script
COPY ./src/consensus/metagraph/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Use entrypoint to start cron and keep the container running
ENTRYPOINT ["./entrypoint.sh"]
