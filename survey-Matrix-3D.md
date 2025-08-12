# Related Works on Matrix-3D: Omnidirectional Explorable 3D World Generation

## Overview

- Matrix-3D is a Skywork AI project that generates omnidirectional, explorable 3D worlds from a single image or text prompt. It uses trajectory-guided panoramic video diffusion and lifts 2D panoramas to 3D via either a fast feed-forward panoramic reconstruction model or an optimization-based 3DGS pipeline. It also introduces the Matrix-Pano dataset for training.

## Related Papers

### 3D World Generation

#### [Matrix-3D: Omnidirectional Explorable 3D World Generation](https://github.com/SkyworkAI/Matrix-3D/blob/main/asset/report.pdf)
- **Venue**: Technical Report (GitHub PDF), 2025
- **Github Page**: [SkyworkAI/Matrix-3D](https://github.com/SkyworkAI/Matrix-3D)
- **Tutorial**: —
- **YouTube Demo**: —
- **Summary**: Presents a panoramic-representation approach for wide-coverage, controllable 3D world generation. A trajectory-guided panoramic video diffusion model produces consistent 360° videos, which are lifted to 3D with two pipelines: a feed-forward panoramic LRM for speed and an optimization-based method for quality. Supports text/image conditioning, fine-grained camera trajectory control, and 360° free exploration; releases a large-scale synthetic panoramic video dataset (Matrix-Pano).
