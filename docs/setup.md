# Setup Instructions

## Prerequisites

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | AMD RX 6000 series | AMD RX 7000 series |
| VRAM | 8GB | 16GB+ |
| RAM | 16GB | 32GB+ |
| Disk Space | 150GB (for all models) | 500GB+ |

### Software Requirements

- **OS**: Linux (Ubuntu 26.04 recommended)
- **Docker**: Latest version with GPU support
- **ROCm Drivers**: 10.0+ installed on host
- **AMD GPU**: RX 6000/7000/9000 series with ROCm support

## Step 1: Install ROCm Drivers

### Ubuntu 26.04

ROCm 10.0 is available in the Ubuntu 26.04 repositories. Install with:

```bash
# Add ROCm repository
curl -fsSL https://repo.radeon.com/rocm/rocm.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/rocm.gpg
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.4 jammy main" | sudo tee /etc/apt/sources.list.d/rocm.list

# Install ROCm
sudo apt update && sudo apt install rocm-dkms

# Add user to required groups
sudo usermod -a -G render,video $USER
```

### Other Distributions

Refer to the [AMD ROCm documentation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start/) for your specific distribution.

## Step 2: Verify ROCm Installation

```bash
# Check ROCm is working
rocm-smi  # Should show your AMD GPU(s)

# Verify device access
ls -la /dev/kfd /dev/dri
```

Expected output for `rocm-smi`:
```
+---------------------------------------------------------------+
| AMDMI Process ID    : 0    Load: 0.00 %                       |
+---------------------------------------------------------------+
| GPU   Temp   Vddc   Fan    Spd   Vddc   Int  Ext   Ref   Pwr |
|       °C             % RPM   mV     A    A     V     W     |
+-------+------+-----+-------+-----+------+------+-----+------+
| 0     XX.XX  XX.X XX.X   XX  XXXX.X XXXX.X XXXX.X 1.234 XXXX |
+-------+------+-----+-------+-----+------+------+-----+------+
```

## Step 3: Clone the Repository

```bash
git clone https://github.com/corundex/comfyui-rocm.git
cd comfyui-rocm
```

## Step 4: Build the Docker Image

### Using build.sh (Recommended)

```bash
# Default build (tag: latest)
chmod +x build.sh
./build.sh

# Custom tag
./build.sh v0.3.43
```

### Direct Docker Build

```bash
docker build -f docker/Dockerfile -t comfyui-rocm:latest .
```

### Build Time Expectations

| Stage | Time |
|-------|------|
| Base image pull | 1-3 minutes |
| ComfyUI clone | 10-30 seconds |
| Dependencies install | 2-5 minutes |
| Total | 5-10 minutes |

## Step 5: Verify the Build

```bash
# Check image exists
docker images | grep comfyui-rocm

# Test GPU access
docker run --rm \
  --device=/dev/kfd --device=/dev/dri --group-add=video \
  corundex/comfyui-rocm:latest python -c "import torch; print(torch.cuda.is_available())"
```

Expected output: `True`

## Step 6: Run ComfyUI

### Quick Run (Single Command)

```bash
docker run -d \
  --name comfyui-rocm \
  --device=/dev/kfd --device=/dev/dri --group-add=video \
  -p 8188:8188 \
  -v ./models:/workspace/ComfyUI/models \
  -v ./output:/workspace/ComfyUI/output \
  corundex/comfyui-rocm:latest
```

### Docker Compose (Recommended for production)

```bash
docker compose up -d
```

### Access ComfyUI

Open your browser and navigate to: **http://localhost:8188**

## Troubleshooting Setup Issues

### ROCm Drivers Not Detected

```bash
# Check driver installation
rocm-smi

# If rocm-smi fails, reinstall drivers
sudo apt install --reinstall rocm-dkms
```

### Container Cannot Access GPU

```bash
# Verify device nodes exist
ls -la /dev/kfd /dev/dri

# Check user is in correct groups
groups $USER
# Should include: render video

# Reboot after driver installation
sudo reboot
```

### Docker GPU Support Not Working

```bash
# Verify nvidia-container-toolkit is NOT installed (conflicts with ROCm)
dpkg -l | grep nvidia

# Verify Docker can see AMD devices
docker run --rm --device=/dev/kfd --device=/dev/dri ubuntu ls /dev/kfd /dev/dri
```

### Build Fails on Dependencies

```bash
# Clear Docker cache and rebuild
docker build --no-cache -f docker/Dockerfile -t comfyui-rocm:latest .

# Check disk space
df -h /var/lib/docker
```

## Next Steps

- See [usage.md](./usage.md) for running and configuring ComfyUI
- See [architecture.md](./architecture.md) for project structure details
- See [overview.md](./overview.md) for project overview
