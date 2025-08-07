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

#### [Neural Game Engine: Accurate learning of generalizable forward models from pixels](https://arxiv.org/abs/2003.10520)
- **Venue**: IEEE Transactions on Games, 2020
- **Github Page**: [Neural-Game-Engine](https://github.com/Bam4d/Neural-Game-Engine)
- **Summary**: This paper introduces the Neural Game Engine (NGE), a novel architecture that learns game dynamics directly from pixel data. It can learn grid-based game environments and generalize to different level sizes, which is highly relevant for creating diverse and scalable interactive worlds like those in Genie 3.

#### [Mastering Atari with Discrete World Models](https://arxiv.org/abs/2010.02193)
- **Venue**: ICLR, 2021
- **Github Page**: [DreamerV2](https://github.com/danijar/dreamerv2)
- **Tutorial**: [DreamerV2 Explained](https://gordicaleksa.medium.com/how-to-get-started-with-reinforcement-learning-rl-4922fafeaf8c)
- **YouTube Demo**: [Dreamer v2 Explained](https://www.youtube.com/watch?v=o75ybZ-6Uu8)
- **Summary**: This paper introduces DreamerV2, a reinforcement learning agent that learns a world model in a discrete latent space. It was the first agent to achieve human-level performance on the Atari benchmark by learning from pixels. This work is highly relevant to Genie 3 as it demonstrates the power of learning a world model for complex, interactive tasks.

#### [Unsupervised learning for physical interaction through video prediction](https://arxiv.org/abs/1605.07157)
- **Venue**: NIPS, 2016
- **Github Page**: [Pytorch Implementation](https://github.com/Xiaohui9607/physical_interaction_video_prediction_pytorch)
- **YouTube Demo**: [NIPS 2016 Spotlight](https://www.youtube.com/watch?v=eYT_9xEu_8g)
- **Summary**: This paper proposes an action-conditioned video prediction model that learns to predict pixel motion to understand physical interactions. By training on unlabeled video, the model learns a representation of physics that can be used for interaction. This is a foundational concept for world models like Genie, which must implicitly learn the physics of their generated worlds to be interactive.

#### [MaskViT: Masked Visual Pre-Training for Video Prediction](https://arxiv.org/abs/2206.11894)
- **Venue**: arXiv, 2022
- **Summary**: This paper introduces MaskViT, a method for pre-training transformers for video prediction using masked visual modeling. By learning to predict missing patches in videos, the model develops a strong understanding of visual dynamics. This is highly relevant to world models like Genie, which need to predict future frames based on actions and current state.- 

#### [CCVS: Context-aware Controllable Video Synthesis](https://arxiv.org/abs/2107.08037)
- **Venue**: NeurIPS, 2021
- **Github Page**: [16lemoing/ccvs](https://github.com/16lemoing/ccvs)
- **Summary**: CCVS proposes a context-aware controllable video synthesis framework that generates future frames while enabling fine-grained control over motion and appearance through context modulation. This work advances controllable video generation, which is central to interactive environment creation in world models like Genie.
- **Github Page**: [agrimgupta92/maskvit](https://github.com/agrimgupta92/maskvit)

#### [Playable Video Generation](https://arxiv.org/abs/2101.12195)
- **Venue**: CVPR, 2021
- **Github Page**: [willi-menapace/PlayableVideoGeneration](https://github.com/willi-menapace/PlayableVideoGeneration)
- **Summary**: This paper introduces Playable Video Generation (PVG), an unsupervised framework that allows users to control the evolution of generated videos. By modelling video dynamics with user inputs, PVG demonstrates controllable, interactive generation of video content, an important step toward creating fully interactive environments as envisioned by Genie.

#### [Playable Environments: Video Manipulation in Space and Time](https://arxiv.org/abs/2203.01914)
- **Venue**: CVPR, 2022
- **Github Page**: [willi-menapace/playable-environments](https://github.com/willi-menapace/playable-environments)
- **Summary**: Playable Environments introduces a framework for interactive video generation and manipulation that allows user control over scene appearance and dynamics in both space and time. This advances real-time controllability in generative video models, directly supporting the creation of interactive worlds as envisioned by Genie.

#### [GAIA-1: A Generative World Model for Autonomous Driving](https://arxiv.org/abs/2309.17080)
- **Venue**: arXiv, 2023
- **Summary**: GAIA-1 is a generative world model specifically for autonomous driving. It can generate realistic driving scenarios from video, text, and action inputs. This work is relevant as it demonstrates the application of world models to a specific, complex, real-world domain, similar to how Genie focuses on creating interactive environments.

#### [Open-Ended Learning Leads to Generally Capable Agents](https://arxiv.org/abs/2107.12808)
- **Venue**: arXiv, 2021
- **Summary**: This DeepMind study trains embodied agents via open-ended learning in a diverse 3D world, showing that broad task exposure leads to strong generalisation and transfer. The results highlight the value of rich, interactive environments—like those generated by Genie—for developing generally capable agents that extend beyond single-task competence.

#### [Learning to Simulate Dynamic Environments with GameGAN](https://arxiv.org/abs/2005.12126)
- **Venue**: CVPR, 2020
- **Github Page**: [nv-tlabs/GameGAN_code](https://github.com/nv-tlabs/GameGAN_code)
- **Summary**: GameGAN is a generative model that learns to visually imitate a game by observing an agent's interactions. It uses a generative adversarial network to learn the game's rules and dynamics from gameplay footage. This is an early example of learning a world model for a game environment, making it a foundational work for later models like Genie.

#### [DriveGAN: Towards a Controllable High-Quality Neural Simulation](https://arxiv.org/abs/2104.15060)
- **Venue**: CVPR, 2021
- **Github Page**: [nv-tlabs/DriveGAN_code](https://github.com/nv-tlabs/DriveGAN_code)
- **Summary**: DriveGAN is a neural simulator that learns from video sequences and agent actions to create a controllable simulation. It achieves controllability by disentangling different components of the environment, such as the background, agent, and other actors. This is highly relevant to Genie's goal of creating interactive and controllable worlds.
#### [Make-A-Video: Text-to-Video Generation without Text-Video Data](https://arxiv.org/abs/2209.14792)
- **Venue**: arXiv, 2022
- **Tutorial**: [Make-A-Video summary](https://medium.com/@curiositydeck/make-a-video-text-to-video-generation-without-text-video-data-summary-74202449e864)
- **Summary**: Make-A-Video extends text-to-image diffusion models to the video domain, enabling text-driven video synthesis without paired text–video training data. It leverages image–text corpora for appearance modeling and uncaptioned videos for temporal consistency, providing a strong baseline for generative video models that informs the visual fidelity goals of Genie-like world models.

#### [Iso-Dream: Isolating and Leveraging Noncontrollable Visual Dynamics in World Models](https://arxiv.org/abs/2205.13817)
- **Venue**: NeurIPS, 2022
- **Github Page**: [panmt/Iso-Dream](https://github.com/panmt/Iso-Dream)
- **Summary**: Iso-Dream extends world-model-based reinforcement learning by disentangling controllable and non-controllable visual dynamics. By isolating elements of the scene that the agent cannot influence, Iso-Dream improves policy learning and prediction accuracy. This work highlights techniques for handling complex dynamics in interactive environments, aligning with Genie's goal of robust world modeling.
#### [Learning Interactive Real-World Simulators (UniSim)](https://arxiv.org/abs/2310.06114)
- **Venue**: arXiv, 2023
- **Project Page**: [universal-simulator.github.io](https://universal-simulator.github.io/)
- **Summary**: UniSim explores training a universal simulator of real-world interactions using video diffusion models. Capable of responding to both high-level instructions and low-level controls, UniSim demonstrates interactive video generation grounded in realistic physics and semantics—advancing the goal of building generally controllable world models like Genie.
#### [From Word Models to World Models: Translating from Natural Language to the Probabilistic Language of Thought](https://arxiv.org/abs/2306.12672)
- **Venue**: arXiv, 2023
#### [NÜWA: Visual Synthesis Pre-Training for Neural Visual World Creation](https://arxiv.org/abs/2111.12417)
- **Venue**: arXiv (to appear in ECCV 2022), 2021
- **Github Page**: [microsoft/NUWA](https://github.com/microsoft/NUWA)
- **YouTube Demo**: [Model Demo](https://www.youtube.com/watch?v=InhMx1h0N40)
- **Summary**: NÜWA is a unified multimodal generative model capable of synthesizing and editing both images and videos from diverse inputs, including text prompts. By pre-training on large-scale visual data and employing a 3D transformer architecture, NÜWA demonstrates strong generalization across visual synthesis tasks, informing the large-scale vision foundation underlying world models like Genie.
- **Summary**: This paper maps natural language descriptions to executable probabilistic programs that capture structured world knowledge, showing how linguistic prompts can be translated into compositional world models. The approach offers insights into bridging text-based user inputs and internal generative models, a key capability for systems like Genie that create interactive environments from textual instructions.
### Large-Scale Vision Models

#### [Scaling Vision Transformers to 22 Billion Parameters](https://arxiv.org/abs/2302.05442)
- **Venue**: ICML, 2023
- **Github Page**: [MegaVIT (Unofficial)](https://github.com/kyegomez/MegaVIT)
- **Tutorial**: [Scaling Image Recognition](https://tmmtt.medium.com/scaling-image-recognition-b77e85e71df1)
- **Summary**: This paper details the training of ViT-22B, the largest dense vision model to date. While not a world model itself, the techniques for training such a large-scale vision model are directly applicable to the development of foundation models like Genie 3, which rely on massive visual processing capabilities.

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