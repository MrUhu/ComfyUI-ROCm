# ComfyUI ROCm - Project Overview

## What is this project?

ComfyUI ROCm is a Docker-based deployment solution for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) with native AMD GPU acceleration using ROCm (Radeon Open Compute). It enables running ComfyUI's node-based AI workflow interface on AMD graphics cards with full GPU compute support.

## Why ROCm?

ComfyUI is traditionally designed for NVIDIA GPUs with CUDA support. This project bridges the gap for AMD GPU owners by:

- Providing a pre-configured ROCm environment with PyTorch 2.13.0
- Including all tested and verified dependencies for AMD hardware
- Offering smart model management with configurable download sets
- Ensuring proper device access (`/dev/kfd`, `/dev/dri`) for ROCm compatibility

## Key Features

| Feature | Description |
|---------|-------------|
| **Node-based AI workflow** | Visual interface for creating complex AI pipelines |
| **AMD ROCm optimized** | Native AMD GPU acceleration with ROCm 10.0+ |
| **Smart model management** | Automatic downloads with configurable model sets |
| **Tested compatibility** | All dependencies verified on real AMD hardware |
| **Ready to use** | Pre-configured with sample workflows |
| **Persistent storage** | Models and outputs preserved across restarts |

## Version Information

| Component | Version |
|-----------|---------|
| Base Image | `rocm/pytorch:rocm10.0_ubuntu26.04_py3.14_pytorch_release_2.13.0` |
| Python | 3.14.0 |
| PyTorch | 2.13.0+git |
| ROCm | 10.0 |
| ComfyUI | latest |

## Supported Hardware

- AMD Radeon RX 6000 series and newer
- AMD Radeon RX 7000 series
- Minimum 8GB VRAM (16GB+ recommended)
- Tested on AMD Radeon RX 9060 XT (16GB VRAM)

## Project Structure

```
ComfyUI-ROCm/
├── docker/                          # Docker configuration
│   ├── Dockerfile                   # Image definition
│   ├── startup.sh                   # Container entrypoint
│   ├── download_models.py           # Model download script
│   ├── models.yaml                  # Model definitions
│   ├── requirements_rocm.txt        # Python dependencies
│   └── sample_workflow.json         # Example ComfyUI workflow
├── build.sh                         # Build script
├── docker-compose.yaml              # Docker Compose configuration
├── README.md                        # Quick start guide
├── AGENTS.md                        # Agent/developer guidelines
└── docs/                            # Extended documentation
    ├── overview.md                  # This file
    ├── setup.md                     # Setup instructions
    ├── usage.md                     # Usage guide
    └── architecture.md              # Architecture documentation
```

## License

This project is licensed under GPL-3.0. See the [LICENSE](../LICENSE) file for details.

## Third-Party Components

- **ComfyUI**: GPL-3.0 - [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- **PyTorch**: BSD 3-Clause - [PyTorch](https://pytorch.org/)
- **ROCm**: Various OSS licenses - [AMD ROCm](https://rocm.docs.amd.com/)
