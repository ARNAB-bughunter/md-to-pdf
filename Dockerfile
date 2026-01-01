FROM public.ecr.aws/lambda/python:3.12

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN dnf update -y && \
    dnf install -y \
    pango \
    pango-devel \
    cairo \
    cairo-devel \
    gdk-pixbuf2 \
    libffi \
    libffi-devel \
    libxml2 \
    libxml2-devel \
    libxslt \
    libxslt-devel \
    fontconfig \
    freetype && \
    dnf clean all

# Set working directory
WORKDIR /var/task

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Lambda entry point
CMD ["app.handler"]