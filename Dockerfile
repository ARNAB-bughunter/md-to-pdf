FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Create non-root user early
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

# Update and install dependencies, then clean up in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    libpango-1.0-0 \
    libpangocairo-1.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory
WORKDIR /md_to_pdf

# Copy requirements first (better caching)
COPY --chown=appuser:appuser requirements.txt .

# Upgrade pip and install dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port (documentation only)
EXPOSE 5000

# Use exec form and drop privileges
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]