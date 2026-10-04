#!/bin/bash
# build.sh - Build ComfyUI ROCm Docker image

set -e

# Configuration
IMAGE_NAME="comfyui-rocm"
VERSION="${1:-latest}"
# Extract base image tag from Dockerfile
BASE_IMAGE_TAG=$(grep '^FROM ' Dockerfile | head -1 | cut -d':' -f2)
DETAILED_TAG="comfyui_${VERSION}__${BASE_IMAGE_TAG}"

echo "🐳 Building ComfyUI ROCm Docker image..."
echo "📦 Tags: ${IMAGE_NAME}:${VERSION}, ${IMAGE_NAME}:${DETAILED_TAG}"
echo ""

# Build the image with both tags
echo "🔨 Building Docker image..."
docker build -f Dockerfile -t "${IMAGE_NAME}:${VERSION}" -t "${IMAGE_NAME}:${DETAILED_TAG}" --progress=plain .
