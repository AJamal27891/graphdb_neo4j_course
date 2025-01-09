FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set timezone noninteractively
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies and add deadsnakes PPA
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    software-properties-common \
    bash \
    sudo \
    curl \
    git \
    wget \
    tzdata \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --set python3 /usr/bin/python3.11

# Install pip for Python 3.11
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Create workspace directory
WORKDIR /workspace

# Copy requirements and install Python packages
COPY requirements.base.txt .
RUN python3.11 -m pip install --no-cache-dir -r requirements.base.txt --ignore-install

# Expose Neo4j-related ports
EXPOSE 7475 7688

CMD ["bash"]