#!/usr/bin/env python3
"""
ComfyUI Model Downloader for RunPod
Easy model download for ComfyUI on RunPod
"""

import os
import sys
import requests
from tqdm import tqdm
from pathlib import Path

# Model save directory / モデル保存先ディレクトリ
MODELS_BASE = Path("/workspace/runpod-slim/ComfyUI/models")

# Hugging Face Token / Hugging Faceトークン
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Model catalog / モデルカタログ
AVAILABLE_MODELS = {
    # ========================================
    # 🔥 Checkpoint Models / チェックポイントモデル
    # ========================================
    "sd15": {
        "url": "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors",
        "filename": "v1-5-pruned.safetensors",
        "dest": "checkpoints",
        "size": "4.27 GB",
        "priority": "HIGH",
        "requires_token": False,
        "description": "Stable Diffusion 1.5 - Most popular model",
        "description_ja": "Stable Diffusion 1.5 - 定番モデル"
    },
    "sd15-ema": {
        "url": "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors",
        "filename": "v1-5-pruned-emaonly.safetensors",
        "dest": "checkpoints",
        "size": "4.27 GB",
        "priority": "HIGH",
        "requires_token": False,
        "description": "SD 1.5 EMA Only - More stable",
        "description_ja": "SD 1.5 EMA Only版 - より安定"
    },
    "sdxl-base": {
        "url": "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors",
        "filename": "sd_xl_base_1.0.safetensors",
        "dest": "checkpoints",
        "size": "6.94 GB",
        "priority": "HIGH",
        "requires_token": False,
        "description": "SDXL Base 1.0 - High resolution",
        "description_ja": "SDXL Base 1.0 - 高解像度"
    },
    "anythingv5": {
        "url": "https://huggingface.co/genai-archive/anything-v5/resolve/main/anything-v5.safetensors",
        "filename": "anythingv5.safetensors",
        "dest": "checkpoints",
        "size": "2.13 GB",
        "priority": "MEDIUM",
        "requires_token": False,
        "description": "Anything V5 - General purpose anime model",
        "description_ja": "Anything V5 - 汎用Animeモデル"
    },
    "realisticvision": {
        "url": "https://huggingface.co/SG161222/Realistic_Vision_V5.1_noVAE/resolve/main/Realistic_Vision_V5.1_fp16-no-ema.safetensors",
        "filename": "realisticvision_v51.safetensors",
        "dest": "checkpoints",
        "size": "2.13 GB",
        "priority": "LOW",
        "requires_token": False,
        "description": "Realistic Vision V5.1 - Photorealistic",
        "description_ja": "Realistic Vision V5.1 - 写実的"
    },
    # ========================================
    # 🚀 New Models / 新モデル (要HF Token)
    # ========================================
    "flux-dev": {
        "url": "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors",
        "filename": "flux1-dev.safetensors",
        "dest": "checkpoints",
        "size": "23.8 GB",
        "priority": "HIGH",
        "requires_token": True,
        "description": "FLUX.1 Dev - Latest high quality model (24GB+ VRAM)",
        "description_ja": "FLUX.1 Dev - 最新高品質モデル (VRAM 24GB以上)"
    },
    "flux-schnell": {
        "url": "https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/flux1-schnell.safetensors",
        "filename": "flux1-schnell.safetensors",
        "dest": "checkpoints",
        "size": "23.8 GB",
        "priority": "MEDIUM",
        "requires_token": True,
        "description": "FLUX.1 Schnell - Fast inference (24GB+ VRAM)",
        "description_ja": "FLUX.1 Schnell - 高速推論 (VRAM 24GB以上)"
    },
    "sd35-large": {
        "url": "https://huggingface.co/stabilityai/stable-diffusion-3.5-large/resolve/main/sd3.5_large.safetensors",
        "filename": "sd3.5_large.safetensors",
        "dest": "checkpoints",
        "size": "16.0 GB",
        "priority": "HIGH",
        "requires_token": True,
        "description": "SD 3.5 Large - Stability AI latest (16GB+ VRAM)",
        "description_ja": "SD 3.5 Large - Stability AI最新 (VRAM 16GB以上)"
    },
    "sd35-medium": {
        "url": "https://huggingface.co/stabilityai/stable-diffusion-3.5-medium/resolve/main/sd3.5_medium.safetensors",
        "filename": "sd3.5_medium.safetensors",
        "dest": "checkpoints",
        "size": "8.9 GB",
        "priority": "HIGH",
        "requires_token": True,
        "description": "SD 3.5 Medium - Balanced (10GB+ VRAM)",
        "description_ja": "SD 3.5 Medium - バランス型 (VRAM 10GB以上)"
    },
    # ========================================
    # ⭐ VAE
    # ========================================
    "vae-mse": {
        "url": "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors",
        "filename": "vae-ft-mse-840000-ema-pruned.safetensors",
        "dest": "vae",
        "size": "335 MB",
        "priority": "MEDIUM",
        "requires_token": False,
        "description": "SD 1.5 VAE - Better colors (Optional)",
        "description_ja": "SD 1.5用 高品質VAE（オプション）"
    },
    "sdxl-vae": {
        "url": "https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors",
        "filename": "sdxl_vae.safetensors",
        "dest": "vae",
        "size": "335 MB",
        "priority": "MEDIUM",
        "requires_token": False,
        "description": "SDXL VAE (Optional)",
        "description_ja": "SDXL用 VAE（オプション）"
    },
}


def download_file(url: str, dest_path: Path, requires_token: bool = False):
    print(f"\n📥 Downloading from / ダウンロード元: {url}")
    print(f"💾 Saving to / 保存先: {dest_path}")

    headers = {}
    if requires_token:
        if not HF_TOKEN:
            raise Exception(
                "HF_TOKEN is required for this model.\n"
                "このモデルにはHugging FaceのAccess Tokenが必要です。"
            )
        headers["Authorization"] = f"Bearer {HF_TOKEN}"
        print("🔑 Using Hugging Face Token / HFトークンを使用中")

    try:
        response = requests.get(url, stream=True, timeout=30, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect / 接続失敗: {e}")

    total_size = int(response.headers.get('content-length', 0))
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with open(dest_path, 'wb') as f, tqdm(
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc=dest_path.name
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

    print(f"✅ Download complete / ダウンロード完了: {dest_path.name}")


def list_models():
    print("\n" + "="*80)
    print("📦 ComfyUI Model Downloader - Available Models")
    print("="*80)

    if HF_TOKEN:
        print("🔑 HF Token detected - Flux/SD3.5 downloads enabled")
    else:
        print("⚠️  No HF Token - Flux/SD3.5 require token (set HF_TOKEN)")

    high_priority = []
    medium_priority = []
    low_priority = []

    for model_id, info in AVAILABLE_MODELS.items():
        priority = info.get('priority', 'LOW')
        if priority == 'HIGH':
            high_priority.append((model_id, info))
        elif priority == 'MEDIUM':
            medium_priority.append((model_id, info))
        else:
            low_priority.append((model_id, info))

    if high_priority:
        print("\n🔥 Main Models / メインモデル:")
        print("-" * 80)
        for model_id, info in high_priority:
            token_mark = "🔑" if info.get('requires_token') else "  "
            print(f"  {token_mark} {model_id:<20} [{info['size']:<10}] {info['filename']}")
            print(f"     └─ {info['description']}")
            print(f"        {info['description_ja']}")

    if medium_priority:
        print("\n⭐ Recommended Models / 推奨モデル:")
        print("-" * 80)
        for model_id, info in medium_priority:
            token_mark = "🔑" if info.get('requires_token') else "  "
            print(f"  {token_mark} {model_id:<20} [{info['size']:<10}] {info['filename']}")
            print(f"     └─ {info['description']}")
            print(f"        {info['description_ja']}")

    if low_priority:
        print("\n💡 Other Models / その他:")
        print("-" * 80)
        for model_id, info in low_priority:
            token_mark = "🔑" if info.get('requires_token') else "  "
            print(f"  {token_mark} {model_id:<20} [{info['size']:<10}] {info['filename']}")
            print(f"     └─ {info['description']}")
            print(f"        {info['description_ja']}")

    print("\n" + "="*80)
    print("🔑 = Requires Hugging Face Token / HFトークンが必要")
    print(f"💾 Save location / 保存先: {MODELS_BASE}/")
    print("="*80)
    print("\nUsage / 使い方:")
    print("  python3 model_downloader.py list")
    print("  python3 model_downloader.py download sd15")
    print("  python3 model_downloader.py url <url> <filename> <dest>")
    print()


def download_model(model_id: str):
    if model_id not in AVAILABLE_MODELS:
        print(f"\n❌ Error: Unknown model ID '{model_id}'")
        print("Run 'python3 model_downloader.py list' to see available models")
        sys.exit(1)

    info = AVAILABLE_MODELS[model_id]
    dest_path = MODELS_BASE / info['dest'] / info['filename']

    if dest_path.exists():
        print(f"\n⚠️  File already exists: {dest_path}")
        response = input("\nOverwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

    try:
        download_file(info['url'], dest_path, requires_token=info.get('requires_token', False))
        print(f"\n✅ Success! Saved to: {dest_path}")
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        if dest_path.exists():
            dest_path.unlink()
        sys.exit(1)


def download_from_url(url: str, filename: str, dest: str = "checkpoints"):
    dest_path = MODELS_BASE / dest / filename

    if dest_path.exists():
        response = input(f"\n⚠️  File exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

    try:
        download_file(url, dest_path)
        print(f"\n✅ Success! Saved to: {dest_path}")
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        if dest_path.exists():
            dest_path.unlink()
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("\n" + "="*80)
        print("ComfyUI Model Downloader for RunPod")
        print("="*80)
        print("\nUsage / 使い方:")
        print("  python3 model_downloader.py list")
        print("  python3 model_downloader.py download <model_id>")
        print("  python3 model_downloader.py url <url> <filename> [dest]")
        print("\nExamples / 例:")
        print("  python3 model_downloader.py download sd15")
        print("  python3 model_downloader.py download flux-dev")
        print("  python3 model_downloader.py url 'https://example.com/model.safetensors' 'model.safetensors' checkpoints")
        print()
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_models()
    elif command == "download":
        if len(sys.argv) < 3:
            print("\n❌ Error: Model ID required")
            sys.exit(1)
        download_model(sys.argv[2])
    elif command == "url":
        if len(sys.argv) < 4:
            print("\n❌ Error: URL and filename required")
            sys.exit(1)
        dest = sys.argv[4] if len(sys.argv) > 4 else "checkpoints"
        download_from_url(sys.argv[2], sys.argv[3], dest)
    else:
        print(f"\n❌ Unknown command: {command}")
        print("Available: list, download, url")
        sys.exit(1)


if __name__ == "__main__":
    main()
