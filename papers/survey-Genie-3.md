# Related Works on Genie 3: A New Frontier for World Models

## Overview

This document provides a survey of related works to Google's Genie 3 model. Genie 3 is a foundation world model that can generate a diversity of interactive environments from text prompts, representing a significant step towards Artificial General Intelligence (AGI). The related works are categorized into foundational models from DeepMind and broader research in AI world models.

## Related Papers

### Foundational DeepMind Models

#### [Genie: Generative Interactive Environments](https://arxiv.org/abs/2402.15391)
- **Venue**: arXiv, 2024
- **Github Page**: [Unofficial PyTorch Implementation](https://github.com/myscience/open-genie)
- **Tutorial**: [DeepMind Genie implementation series 1 — base structure](https://dohyeongkim.medium.com/deepmind-genie-implementation-series-1-base-structure-47727338cc1a)
- **Summary**: The original paper for the Genie model, introducing a foundation world model trained on internet videos that can generate interactive 2D platformer games from a single image prompt. It is the direct predecessor to Genie 2 and 3.

#### [Genie 2: A large-scale foundation world model](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/)
- **Venue**: Google DeepMind Blog, 2024
- **Summary**: Genie 2 expands on the original Genie by generating a wider variety of action-controllable, playable 3D environments. It is a key step towards the real-time, high-resolution capabilities of Genie 3.

#### [Veo 3 Tech Report](https://storage.googleapis.com/deepmind-media/veo/Veo-3-Tech-Report.pdf)
- **Venue**: Google DeepMind, 2024
- **Summary**: Veo 3 is Google's most capable video generation model. While not a world model in the same interactive sense as Genie, its advancements in video generation, consistency, and understanding of cinematic techniques are foundational to the high-fidelity visual output of Genie 3.

#### [Scaling Instructable Agents Across Many Simulated Worlds](https://arxiv.org/abs/2404.10179)
- **Venue**: arXiv, 2024
- **Github Page**: [Unofficial PyTorch Implementation](https://github.com/kyegomez/SIMA)
- **Tutorial**: [谷歌发布了可以玩3D游戏的通用AI智能体SIMA](https://zhuanlan.zhihu.com/p/687104325)
- **Summary**: The SIMA project focuses on training generalist AI agents that can follow natural language instructions across a wide range of 3D virtual environments. This is highly relevant to Genie 3, which provides the ideal training grounds for such agents.

### AI World Models and Generative Environments

#### [Toward Stable World Models: Measuring and Enhancing World Stability](https://arxiv.org/abs/2503.08122)
- **Venue**: arXiv, 2025
- **Summary**: This paper introduces the concept of "World Stability" and proposes methods to measure and enhance the content preservation capabilities of world models. This is crucial for the temporal consistency seen in Genie 3.

#### [A world model: On the political logics of generative AI](https://www.sciencedirect.com/science/article/pii/S0962629824000830)
- **Venue**: ScienceDirect, 2024
- **Summary**: This article discusses the broader implications of generative AI creating "world models," including the political and governing rationalities that arise. It provides a critical perspective on the societal impact of technologies like Genie 3.

### Navigable and Interactive Environments

#### [A Survey of Interactive Generative Video](https://arxiv.org/abs/2504.21853)
- **Venue**: arXiv, 2025
- **YouTube Demo**: [AI Video You Can Control: IGV Explained](https://www.youtube.com/watch?v=fXcBCVXVcqI)
- **Summary**: This survey provides a roadmap of real-time video generation systems for gaming, embodied AI, and driving. It focuses on the combination of generative capabilities with interactive features, which is the core of navigable world models like Genie.

#### [How People Prompt Generative AI to Create Interactive VR Scenes](https://dl.acm.org/doi/10.1145/3643834.3661547)
- **Venue**: DIS 2024: Conference on Designing Interactive Systems 2024
- **Summary**: This paper explores how users interact with generative AI to create interactive VR scenes. It provides insights into the user-experience side of creating navigable and interactive worlds, which is a key application area for Genie-like models.
### OpenAI's Contributions

#### [Video generation models as world simulators](https://openai.com/index/video-generation-models-as-world-simulators/)
- **Venue**: OpenAI Blog, 2024
- **Github Page**: [Open-Sora-Plan (Unofficial)](https://github.com/PKU-YuanGroup/Open-Sora-Plan)
- **Tutorial**: [How to Generate Videos with Open-Sora-Plan](https://medium.com/data-science/how-to-generate-videos-with-open-sora-plan-video-generation-model-fdee4151ec90)
- **Summary**: This blog post introduces Sora, OpenAI's text-to-video model. While not explicitly an interactive world model like Genie, Sora's ability to generate long, coherent video sequences with a high degree of physical realism makes it a significant contribution to the development of world simulators. It demonstrates a different, but related, path towards building general-purpose simulators of the physical world.