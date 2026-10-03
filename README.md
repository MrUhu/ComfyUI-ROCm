# ComfyUI ROCm Docker Image

Docker-based deployment of ComfyUI with AMD ROCm GPU acceleration.

[![Docker Pulls](https://img.shields.io/docker/pulls/corundex/comfyui-rocm)](https://hub.docker.com/r/corundex/comfyui-rocm) [![ROCm](https://img.shields.io/badge/ROCm-10.0-blue)](https://rocm.docs.amd.com/) [![Python](https://img.shields.io/badge/Python-3.14-blue)](https://www.python.org/)

![ComfyUI Interface](Screenshot.png)
*ComfyUI running on AMD ROCm with sample workflow and generated landscape image*

## Version Information

| Component | Version |
|-----------|---------|
| Base Image | `rocm/pytorch:rocm10.0_ubuntu26.04_py3.14_pytorch_release_2.13.0` |
| Python | 3.14.0 |
| PyTorch | 2.13.0+git |
| ROCm | 10.0 |
| ComfyUI | latest (git clone) |

## Features

- Node-based AI workflow interface
- AMD ROCm GPU acceleration
- Smart model management with configurable download sets
- Pre-configured sample workflows
- Persistent storage for models and outputs
- Health-checked Docker Compose support

## Building the Image

This project is primarily intended for building your own Docker image from source.

```bash
# Build with default tag (latest)
./build.sh

# Build with custom tag
./build.sh v0.3.43
```

The build script tags the image with both the simple version and a detailed tag combining the app version with the base image tag (e.g., `comfyui_rocm_v0.3.43__rocm10.0_ubuntu26.04_py3.14_pytorch_release_2.13.0`).

Alternatively, build directly:

```bash
docker build -f Dockerfile -t comfyui-rocm:latest .
```

Or pull the pre-built image from Docker Hub:

```bash
docker pull corundex/comfyui-rocm:latest
```

## Running the Container

```bash
docker run -d \
  --name comfyui-rocm \
  --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 \
  -e CUDA_VISIBLE_DEVICES="" \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest
```

Access ComfyUI at: **http://localhost:8188**

> **Quick Start:** Add `-e MODEL_DOWNLOAD=default` to download ~17.3 GB of default models on first run. Subsequent runs will skip already-downloaded models.

## Requirements

| Component | Requirement |
|-----------|-------------|
| GPU | AMD Radeon RX 9060 XT (tested) |
| VRAM | 8GB minimum (16GB+ recommended) |
| OS | Linux with `amdgpu` kernel module |
| Docker | Latest version with `/dev/kfd` access |
| Kernel | Any with `amdgpu` module (modprobe amdgpu if needed) |

## Setup

### 1. Verify AMD GPU Support

The container includes all ROCm userspace libraries. The host only needs kernel-level AMD GPU support.

```bash
# Check if amdgpu is loaded
lsmod | grep amdgpu
```

If not loaded:

```bash
sudo modprobe amdgpu
```

Add your user to required groups:

```bash
sudo usermod -a -G render,video $USER
# Log out and back in for group changes to take effect
```

Verify device nodes exist:

```bash
ls -l /dev/kfd /dev/dri
```

> **Note:** You do NOT need to install ROCm userspace packages (`rocm-dkms`, `rocm-smi`, etc.) on the host. The Docker container includes all necessary ROCm libraries.

### 2. Verify GPU Access

```bash
docker exec comfyui-rocm python -c "import torch; print(torch.cuda.is_available())"
```

Expected output: `True`

### 3. Run ComfyUI

```bash
docker run -d \
  --name comfyui-rocm \
  --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 \
  -e CUDA_VISIBLE_DEVICES="" \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest
```

## Model Management

Control model downloading with the `MODEL_DOWNLOAD` environment variable. Models are downloaded on first run and cached in the mounted volumes.

> **Important:** By default, **no models are downloaded** on first run. Set `MODEL_DOWNLOAD` to trigger downloads. See options below.

| Mode | Size | Models |
|------|------|--------|
| `""` (empty/unset) | No download | - | **Default** - Container starts with no models, user must set `MODEL_DOWNLOAD` to trigger downloads |
| `default` | ~17.3 GB | FLUX.1 Dev FP8, Flux VAE (ae.safetensors) |
| `common` | ~41.4 GB | FLUX.1 Schnell, SD VAE FT MSE, Flux VAE, RealESRGAN x4plus, RealESRGAN x4plus Anime, EasyNegative, Flux Canny ControlNet V3, Flux Depth ControlNet V3 |
| `realistic` | ~13.5 GB | Juggernaut XL v9, Juggernaut XL Lightning, SD VAE FT MSE |
| `photorealistic` | ~31.3 GB | SD3.5 Medium, FLUX.1 Dev FP8, Flux HED ControlNet V3, SD VAE FT MSE |
| `artistic` | ~22.7 GB | FLUX.1 Schnell, SD3.5 Medium, Flux Depth ControlNet Dev LoRA, SD VAE FT MSE |
| `pixelart` | ~9.1 GB | Pixel Art XL, All-In-One Pixel Model, Pixel Art LoRA, SD VAE FT MSE |
| `all` | ~135.3 GB | All sets combined |
| `none` | 0 GB | No downloads |

### First Run Setup

By default, the container starts with **no models downloaded**. To download models on first run:

```bash
# Download default models (~17.3 GB)
docker run -d --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 -e MODEL_DOWNLOAD=default -e CUDA_VISIBLE_DEVICES="" \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest
```

### Triggering Additional Downloads

If you already have models mounted and want to download additional sets:

```bash
# Stop container
docker stop comfyui-rocm

# Update MODEL_DOWNLOAD and restart
docker run -d --name comfyui-rocm \
  --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 -e MODEL_DOWNLOAD=realistic -e CUDA_VISIBLE_DEVICES="" \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest
```

Models that already exist are skipped (checked by file size), so you can safely change `MODEL_DOWNLOAD` to add new model sets without re-downloading existing ones.

### Usage Examples

```bash
# Default models (~17.3 GB download on first run)
docker run -d --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 -e CUDA_VISIBLE_DEVICES="" \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest

# Realistic photo models (~13.5 GB)
docker run -d --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 -e MODEL_DOWNLOAD=realistic -e CUDA_VISIBLE_DEVICES="" \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest

# All models (~135.3 GB download)
docker run -d --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 -e MODEL_DOWNLOAD=all -e CUDA_VISIBLE_DEVICES="" \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest

# No downloads (use existing models only)
docker run -d --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 -e MODEL_DOWNLOAD=none -e CUDA_VISIBLE_DEVICES="" \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest
```

## Docker Compose

```yaml
services:
  comfyui-rocm:
    image: corundex/comfyui-rocm:latest
    pull_policy: always
    container_name: comfyui-rocm
    hostname: comfyui-rocm

    # GPU access for AMD ROCm
    devices:
      - /dev/kfd:/dev/kfd
      - /dev/dri:/dev/dri

    # Add video group for GPU access
    group_add:
      - video

    # Port mapping
    ports:
      - "8188:8188"

    # Volume mapping
    volumes:
      - ./data/models:/workspace/ComfyUI/models
      - ./data/output:/workspace/ComfyUI/output
      - ./data/input:/workspace/ComfyUI/input
      - ./data/custom_nodes:/workspace/ComfyUI/custom_nodes
      - ./data/user:/workspace/ComfyUI/user
      - ./data/temp:/workspace/ComfyUI/temp

    # Environment variables
    environment:
      - MODEL_DOWNLOAD=none    # Change to 'default', 'realistic', etc. to download models
      - HIP_VISIBLE_DEVICES=0
      - CUDA_VISIBLE_DEVICES=""

    # Restart policy
    restart: unless-stopped

    # Healthcheck
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8188/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s
```

Run with: `docker compose up -d`

## Performance

### Tested Hardware

- AMD Radeon RX 9060 XT (16GB VRAM)

### Performance Metrics

- Generation Time: ~30-60s for 512x512 images
- VRAM Usage: 4-8GB for basic operations
- Model Loading: ~30-60s first time, cached afterward
- Batch Processing: Multiple images supported

### Tips

- Mount persistent volumes to avoid re-downloading models
- Start with `default` models, upgrade to larger sets as needed
- Use fast SSD storage for optimal model loading

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Container won't start | Check kernel modules: `lsmod | grep amdgpu` |
| No GPU detected | Verify GPU access: `docker exec comfyui-rocm python -c "import torch; print(torch.cuda.is_available())"` |
| Model download fails | Check internet connection, disk space, and container logs |
| Out of memory | Reduce batch size, use smaller models, ensure 8GB+ VRAM |
| Models not found | Verify downloads completed and file permissions |

## License & Credits

This project is licensed under GPL-3.0. See the [LICENSE](LICENSE) file for details.

### Third-Party Components

- **ComfyUI**: GPL-3.0 - [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- **PyTorch**: BSD 3-Clause - [PyTorch](https://pytorch.org/)
- **ROCm**: Various OSS licenses - [AMD ROCm](https://rocm.docs.amd.com/)

---

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-corundex%2Fcomfyui--rocm-blue)](https://hub.docker.com/r/corundex/comfyui-rocm) [![GitHub](https://img.shields.io/badge/GitHub-corundex%2Fcomfyui--rocml-181717)](https://github.com/corundex/comfyui-rocm) [![ComfyUI](https://img.shields.io/badge/ComfyUI-comfyanonymous%2Fcomfyui-181717)](https://github.com/comfyanonymous/ComfyUI)
