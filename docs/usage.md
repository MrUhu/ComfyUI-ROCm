# Usage Guide

## Running ComfyUI

### Docker Run

```bash
docker run -d \
  --name comfyui-rocm \
  --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest
```

### Docker Compose

```bash
docker compose up -d
```

### Access the Interface

- **Web UI**: http://localhost:8188
- **API**: http://localhost:8188/api
- **WebSocket**: ws://localhost:8188/ws

## Environment Variables

| Variable | Values | Default | Description |
|----------|--------|---------|-------------|
| `MODEL_DOWNLOAD` | `default`, `common`, `realistic`, `photorealistic`, `artistic`, `all`, `none` | `default` | Control which models to download |
| `HIP_VISIBLE_DEVICES` | GPU index (0, 1, 2...) | `0` | Select which GPU to use |
| `CUDA_VISIBLE_DEVICES` | Must be empty string | `""` | Must be empty for ROCm to work |

### Setting Environment Variables

```bash
# Via docker run
docker run -d \
  --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 \
  -e MODEL_DOWNLOAD=common \
  -e HIP_VISIBLE_DEVICES=0 \
  -e CUDA_VISIBLE_DEVICES="" \
  -v ./models:/workspace/ComfyUI/models \
  corundex/comfyui-rocm:latest

# Via docker-compose.yaml
environment:
  - MODEL_DOWNLOAD=common
  - HIP_VISIBLE_DEVICES=0
  - CUDA_VISIBLE_DEVICES=""
```

## Model Management

### Model Download Modes

| Mode | Size | Models Included |
|------|------|-----------------|
| `default` | ~4GB | SD 1.5 |
| `common` | ~30GB | SD 1.5, SDXL, ControlNets, upscalers, VAE, embeddings |
| `realistic` | ~8GB | Realistic Vision, DreamShaper, VAE |
| `photorealistic` | ~12GB | Juggernaut XL, RealVisXL |
| `artistic` | ~2GB | Deliberate v2 |
| `all` | ~100GB | All model sets combined |
| `none` | 0GB | Skip downloads, use existing models only |

### Custom Model Downloads

To add custom models:

1. Edit [`artifacts/workspace/models.yaml`](../artifacts/workspace/models.yaml)
2. Add entries under a new section or existing section
3. Rebuild the image: `./build.sh`
4. Run with `MODEL_DOWNLOAD=your_section_name`

### Model Directory Structure

```
/workspace/ComfyUI/models/
├── checkpoints/        # Main model files (.safetensors, .ckpt)
├── vae/                # VAE models
├── loras/              # LoRA adapters
├── embeddings/         # Textual inversion embeddings
├── upscale_models/     # Super-resolution models
└── controlnet/         # ControlNet models
```

## Volume Mounts

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./models` | `/workspace/ComfyUI/models` | Model files (persistent) |
| `./output` | `/workspace/ComfyUI/output` | Generated images |
| `./input` | `/workspace/ComfyUI/input` | Input images |
| `./custom_nodes` | `/workspace/ComfyUI/custom_nodes` | Custom node installations |
| `./user` | `/workspace/ComfyUI/user` | User settings and workflows |

### Recommended Docker Compose Volumes

```yaml
volumes:
  - ./data/models:/workspace/ComfyUI/models
  - ./data/output:/workspace/ComfyUI/output
  - ./data/input:/workspace/ComfyUI/input
  - ./data/custom_nodes:/workspace/ComfyUI/custom_nodes
  - ./data/user:/workspace/ComfyUI/user
```

## Container Management

### Start/Stop/Restart

```bash
# Start
docker start comfyui-rocm

# Stop
docker stop comfyui-rocm

# Restart
docker restart comfyui-rocm

# Docker Compose
docker compose start
docker compose stop
docker compose restart
```

### View Logs

```bash
# Live logs
docker logs -f comfyui-rocm

# Last 100 lines
docker logs --tail 100 comfyui-rocm

# Docker Compose
docker compose logs -f
```

### Execute Commands Inside Container

```bash
# Python GPU check
docker exec comfyui-rocm python -c "import torch; print(torch.cuda.is_available())"

# List models
docker exec comfyui-rocm ls -la /workspace/ComfyUI/models/checkpoints/

# Install a custom node
docker exec -it comfyui-rocm git clone https://github.com/user/custom-node /workspace/ComfyUI/custom_nodes/custom-node
```

### Remove Container

```bash
docker stop comfyui-rocm && docker rm comfyui-rocm
```

## Performance Tips

### Optimization

| Tip | Impact |
|-----|--------|
| Use fast SSD storage | Faster model loading |
| Mount persistent volumes | Avoid re-downloading models |
| Start with `default` models | Save disk space initially |
| Use `HIP_VISIBLE_DEVICES` | Pin to specific GPU in multi-GPU systems |

### VRAM Management

```bash
# Monitor VRAM usage inside container
docker exec comfyui-rocm rocm-smi

# Typical VRAM usage
# - SD 1.5 (512x512): 4-6GB
# - SDXL (1024x1024): 6-10GB
# - With ControlNet: +2-4GB
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Container won't start | Check ROCm drivers: `rocm-smi` |
| No GPU detected | Verify container GPU access: `docker exec comfyui-rocm python -c "import torch; print(torch.cuda.is_available())"` |
| Model download fails | Check internet connection, disk space, and logs |
| Out of memory | Reduce batch size, use smaller models, ensure 8GB+ VRAM |
| Models not found | Verify downloads completed and file permissions |

### Debug Mode

```bash
# Run with verbose output
docker run -it \
  --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 \
  -e MODEL_DOWNLOAD=none \
  corundex/comfyui-rocm:latest /bin/bash

# Inside container, run startup manually
bash /workspace/startup.sh
```

### Health Check

```bash
# Check if ComfyUI is responding
curl http://localhost:8188/

# Check container health
docker inspect --format='{{.State.Health.Status}}' comfyui-rocm
```

## Updating

### Pull Latest Image

```bash
docker pull corundex/comfyui-rocm:latest
docker stop comfyui-rocm && docker rm comfyui-rocm
docker run [your original run command]
```

### Rebuild from Source

```bash
git pull
./build.sh
```

## Next Steps

- See [overview.md](./overview.md) for project overview
- See [setup.md](./setup.md) for setup instructions
- See [architecture.md](./architecture.md) for architecture details
