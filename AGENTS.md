# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Critical

### Change Documentation Requirement

**All code changes MUST be documented.** When modifying any functionality:

1. Update the relevant documentation in `docs/`:
2. Update this `AGENTS.md` if any critical gotchas or commands change
3. Update `README.md` quick-start section if public-facing behavior changes

Failure to document changes will result in incomplete PRs.

**Changes MUST be validated.**
Run `git add . && pre-commit run --all-files` whenever a modification happend.

## Project Overview

Docker-based deployment for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) with AMD ROCm GPU support. This is a **Docker image project**, not a traditional codebase. The `docker/` directory contains the Dockerfile, startup scripts, and model configuration.

## Build Commands

```bash
# Build with build.sh (default tag: latest)
./build.sh

# Build with custom tag
./build.sh v0.3.43

# Direct docker build
docker build -f docker/Dockerfile -t comfyui-rocm:latest .
```

## Run Commands

```bash
# Docker run (minimal)
docker run -d \
  --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest

# Docker Compose
docker compose up -d

# Verify GPU access inside container
docker exec comfyui-rocm python -c "import torch; print(torch.cuda.is_available())"
```

## Environment Variables

| Variable | Values | Default |
|----------|--------|---------|
| `MODEL_DOWNLOAD` | `default`, `common`, `realistic`, `photorealistic`, `artistic`, `all`, `none` | `default` |
| `HIP_VISIBLE_DEVICES` | GPU index | `0` |
| `CUDA_VISIBLE_DEVICES` | Must be empty for ROCm | `""` |

## Version Information

| Component | Version |
|-----------|---------|
| Base Image | `rocm/pytorch:rocm10.0_ubuntu26.04_py3.14_pytorch_release_2.13.0` |
| Python | 3.14.0 |
| PyTorch | 2.13.0+git |
| ROCm | 10.0 |

## Key Paths (inside container)

- ComfyUI: `/workspace/ComfyUI/`
- Models config: `/workspace/models.yaml`
- Download script: `/workspace/download_models.py`
- Startup script: `/workspace/startup.sh`

## Critical Gotchas

- **ROCm requires `--device=/dev/kfd`** - standard `--gpus all` does NOT work for AMD GPUs
- `CUDA_VISIBLE_DEVICES` must be empty string (`""`), not unset, to avoid PyTorch CUDA conflicts
- Models directory structure: `/workspace/ComfyUI/models/{checkpoints,vae,loras,embeddings,upscale_models,controlnet}`
- `requirements_rocm.txt` uses inline comments (`✅`, `❌`, `📦`) to mark package compatibility - respect these markers
- The base image (`rocm/pytorch`) already includes torch, torchvision, numpy, scipy, tqdm, psufind, aiohttp, yarl, soundfile - do NOT reinstall these
