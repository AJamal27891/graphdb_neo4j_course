FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set timezone
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3-pip \
    htop \
    nano \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --set python3 /usr/bin/python3.11

# Install pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Set workspace
WORKDIR /workspace

# Install requirements
COPY requirements*.txt ./

# Install PyTorch with CUDA 11.8 support (explicit version match)
RUN python3.11 -m pip install --no-cache-dir \
    torch==2.0.1+cu118 \
    torchvision==0.15.2+cu118 \
    torchaudio==2.0.2+cu118 \
    --extra-index-url https://download.pytorch.org/whl/cu118

# Install geometric packages FIRST using PyG's official binaries:cite[3]:cite[5]
RUN python3.11 -m pip install --no-cache-dir \
    -r requirements.geometric.txt \
    --find-links=https://data.pyg.org/whl/torch-2.0.1+cu118.html

# Install other requirements separately
RUN python3.11 -m pip install --no-cache-dir \
    -r requirements.base.txt
    
CMD ["bash"]