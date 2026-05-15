# 🎨 ComfyUI Model Downloader for RunPod

Easy model downloader for RunPod's official ComfyUI template.  
RunPod公式ComfyUIテンプレート用のモデルダウンローダーです。

## 🚀 使い方 / How to Use

RunPodのComfyUIテンプレートを起動後、JupyterLab（ポート8888）のターミナルで以下を実行：

```bash
wget -O /workspace/Download_Models.ipynb https://raw.githubusercontent.com/sakasa15/comfyui-model-downloader/main/Download_Models.ipynb
```

その後、`Download_Models.ipynb` をJupyterLabで開いて▶を押すだけ！

## 📦 対応モデル / Supported Models

| モデル | サイズ | VRAM | 備考 |
|--------|--------|------|------|
| SD 1.5 | 4.27 GB | 6GB+ | |
| SDXL Base | 6.94 GB | 12GB+ | |
| FLUX.1 Dev | 23.8 GB | 24GB+ | 🔑 |
| FLUX.1 Schnell | 23.8 GB | 24GB+ | 🔑 |
| SD 3.5 Large | 16.0 GB | 16GB+ | 🔑 |
| SD 3.5 Medium | 8.9 GB | 10GB+ | 🔑 |
| Anything V5 | 2.13 GB | 6GB+ | |
| Realistic Vision V5.1 | 2.13 GB | 6GB+ | |
| VAE (SD1.5) | 335 MB | - | |
| VAE (SDXL) | 335 MB | - | |

🔑 = Hugging Face Token が必要 / Required

## 🔑 Hugging Face Token

FluxやSD3.5のダウンロードには [Hugging Face Access Token](https://huggingface.co/settings/tokens) と各モデルページでのライセンス同意が必要です。

## 📄 License

MIT License
