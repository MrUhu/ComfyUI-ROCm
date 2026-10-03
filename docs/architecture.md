# Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Host System                              │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │ ROCm Drivers │    │ Docker Engine    │    │ AMD GPU       │  │
│  │ (10.0+)      │    │                  │    │ (/dev/kfd     │  │
│  └──────┬───────┘    │  ┌────────────┐  │    │ /dev/dri)     │  │
│         │            │  │ Container  │  │    └───────────────┘  │
│         │            │  │            │  │                      │  │
│         └────────────┼──┤  ComfyUI   │  │                      │  │
│                      │  │  PyTorch   │  │                      │  │
│                      │  │  ROCm      │  │                      │  │
│                      │  └────────────┘  │                      │  │
│                      └──────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

## Container Architecture

### Image Layers

```
rocm/pytorch:rocm10.0_ubuntu26.04_py3.14_pytorch_release_2.13.0
├── Ubuntu 26.04 base
├── ROCm 10.0 libraries
├── PyTorch 2.13.0 with ROCm support
├── Python 3.14
├── System dependencies (git, wget, curl)
├── ComfyUI source code
├── ROCm-compatible Python packages
├── Startup scripts & model config
└── Model directories
```

### Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                     Container Startup                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  startup.sh                                                 │
│  │                                                          │
│  ├──► download_models.py                                    │
│  │      │                                                    │
│  │      ├── Reads models.yaml                               │
│  │      ├── Checks MODEL_DOWNLOAD env var                   │
│  │      ├── Downloads required models                       │
│  │      └── Validates file sizes                            │
│  │                                                          │
│  └──► python main.py                                       │
│         │                                                    │
│         └──► ComfyUI Server                                 │
│               ├── HTTP API (port 8188)                       │
│               ├── WebSocket (port 8188)                      │
│               └── PyTorch/ROCm GPU inference                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

### Inside Container

```
/workspace/
├── ComfyUI/                          # ComfyUI source
│   ├── main.py                       # Entry point
│   ├── requirements.txt              # ComfyUI deps
│   └── [ComfyUI source files]
│
├── requirements_rocm.txt             # ROCm-compatible packages
├── startup.sh                        # Container entrypoint
├── download_models.py                # Model download script
├── models.yaml                       # Model definitions
└── ComfyUI/models/                   # Model storage
    ├── checkpoints/
    ├── vae/
    ├── loras/
    ├── embeddings/
    ├── upscale_models/
    └── controlnet/
```

### Project Structure (Host)

```
ComfyUI-ROCm/
├── artifacts/                        # Docker configuration
│   ├── Dockerfile                    # Image definition
│   ├── startup.sh                    # Container entrypoint
│   ├── download_models.py            # Model download script
│   ├── models.yaml                   # Model definitions
│   ├── requirements_rocm.txt         # Python dependencies
│   ├── comfyui/                      # ComfyUI files
│   │   └── sample_workflow.json      # Example workflow
│   └── .dockerignore
├── build.sh                          # Build script
├── docker-compose.yaml               # Docker Compose config
├── README.md                         # Quick start
├── AGENTS.md                         # Developer guidelines
├── LICENSE
└── docs/                             # Documentation
    ├── overview.md
    ├── setup.md
    ├── usage.md
    └── architecture.md
```

## Key Components

### [`Dockerfile`](../Dockerfile)

Defines the Docker image layers:
1. Starts from `rocm/pytorch` base image
2. Installs system dependencies (git, wget, curl)
3. Clones ComfyUI repository
4. Creates model directory structure
5. Installs Python dependencies from `requirements_rocm.txt`
6. Copies startup scripts and model config
7. Sets health check and entrypoint

### [`artifacts/workspace/startup.sh`](../artifacts/workspace/startup.sh)

Container entrypoint script:
1. Runs `download_models.py` to fetch configured models
2. Starts ComfyUI with `python main.py --listen 0.0.0.0 --port 8188`
3. Passes through any additional arguments (`$@`)

### [`artifacts/workspace/download_models.py`](../artifacts/workspace/download_models.py)

Model download manager:
1. Reads `models.yaml` configuration
2. Checks `MODEL_DOWNLOAD` environment variable
3. Downloads models to correct paths
4. Validates file sizes against `min_size` thresholds
5. Skips already downloaded models

### [`artifacts/workspace/models.yaml`](../artifacts/workspace/models.yaml)

Model definitions in YAML format:
- Organized by download mode (`default`, `common`, `realistic`, etc.)
- Each model has: name, URL, path, minimum size
- Paths are relative to `/workspace/ComfyUI/models/`

### [`artifacts/workspace/requirements_rocm.txt`](../artifacts/workspace/requirements_rocm.txt)

Python package requirements with ROCm compatibility markers:
- `✅` - Confirmed working on ROCm
- `❌` - Not compatible with ROCm
- `📦` - Safe to install

### [`docker-compose.yaml`](../docker-compose.yaml)

Docker Compose configuration for production deployment:
- Device mappings for GPU access
- Volume mounts for persistence
- Environment variable configuration
- Restart policy

## Data Flow

### Model Download Flow

```
Container Start
     │
     ▼
startup.sh
     │
     ▼
download_models.py
     │
     ├── Read MODEL_DOWNLOAD env var
     │
     ├── Load models.yaml
     │
     ├── Select models for download mode
     │
     ├── For each model:
     │    ├── Check if file exists
     │    ├── Validate file size >= min_size
     │    └── Download if missing/invalid
     │
     └── Exit (success)
     │
     ▼
python main.py (ComfyUI)
```

### Request Flow

```
Browser
     │
     ▼
HTTP Request (port 8188)
     │
     ▼
ComfyUI Server
     │
     ├── Queue workflow
     │
     ├── Execute nodes
     │    │
     │    ├── Load model from disk
     │    │
     │    └── PyTorch inference (ROCm)
     │         │
     │         └── GPU compute (/dev/kfd)
     │
     ▼
Response (JSON)
     │
     ▼
Browser (displays result)
```

## Dependency Chain

```
rocm/pytorch base image
├── ROCm 10.0 libraries
│   ├── HIP runtime
│   ├── rocBLAS
│   ├── MIOpen
│   └── rcCL
├── PyTorch 2.13.0
│   └── ROCm backend
├── Python 3.14
│   └── pip packages (from requirements_rocm.txt)
│       ├── numpy, scipy
│       ├── Pillow, imageio
│       ├── requests, aiohttp
│       ├── transformers, diffusers
│       └── [ROCm-compatible packages]
└── ComfyUI
    └── Custom node support via /workspace/ComfyUI/custom_nodes
```

## Security Considerations

| Aspect | Configuration |
|--------|---------------|
| Device access | Only `/dev/kfd` and `/dev/dri` (no full host access) |
| Network | Binds to `0.0.0.0:8188` (use reverse proxy for production) |
| File permissions | Runs as root in container (standard for Docker) |
| Volumes | Read/write access to mounted directories |

## Extending the Architecture

### Adding Custom Nodes

```bash
# Method 1: Direct clone
docker exec -it comfyui-rocm git clone <node-repo> /workspace/ComfyUI/custom_nodes/<node-name>

# Method 2: Via volume mount
# Create ./custom_nodes/<node-name> on host
# Mount in docker-compose.yaml
```

### Adding Custom Models

```bash
# Place model files in mounted volume
./models/checkpoints/your-model.safetensors

# Or add to models.yaml for automated download
```

### Customizing the Build

```bash
# Modify Dockerfile for custom base image
# Add custom apt packages or pip installs
# Rebuild: ./build.sh
```

## Next Steps

- See [overview.md](./overview.md) for project overview
- See [setup.md](./setup.md) for setup instructions
- See [usage.md](./usage.md) for usage guide
