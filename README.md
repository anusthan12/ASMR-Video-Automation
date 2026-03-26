<div align="center">

# 🎧 Automated ASMR Content Creator & YouTube Uploader

**A fully autonomous, end-to-end AI content pipeline — from concept generation to scheduled YouTube publication — built without a single manual step.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![YouTube Data API](https://img.shields.io/badge/YouTube_API-v3-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](#)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-Authenticated-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](#)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Powered-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)](#)
[![Status](https://img.shields.io/badge/Status-Discontinued-lightgrey?style=for-the-badge)](#️-important-notice--service-discontinuation)

</div>

<br />

> **This project's automated services have been discontinued** following regulatory changes in India affecting monetization of AI-generated video content on YouTube. The full codebase is preserved here for **educational and technical reference**. See the [notice below](#️-important-notice--service-discontinuation) for details.

---

## 📖 Overview

This repository contains the source code for a production-grade, fully automated ASMR content generation and distribution system. The system operated as a self-sustaining pipeline — interpreting themes, synthesizing audio and visuals, encoding production-ready video, and publishing to YouTube on a fixed **8-hour schedule** — with zero manual intervention at any stage.

The goal was not just automation, but *intelligent* automation: a system capable of producing contextually coherent, high-quality ASMR content at machine speed and human scale.

---

## ✨ System Architecture & End-to-End Pipeline

The automation was structured as a sequential, fault-tolerant pipeline across four distinct stages:

### Stage 1 — Content Conceptualization
- Interprets pre-defined content themes or dynamic user prompts to generate ASMR scenarios.
- Determines audio texture profiles (whisper narratives, ambient soundscapes, layered effects).
- Selects or generates complementary visual motifs (abstract animations, calming patterns, synchronized object movements).

### Stage 2 — Audio & Visual Synthesis
- **Audio:** Generates whispered narration via TTS engines and layers synthesized ambient effects (tapping, crinkling, rainfall, crackling fire) using `Pydub` / `AudioSegment` for precise mixing, EQ, and stereo spatialization.
- **Visual:** Produces or assembles visual elements frame-by-frame, timed to audio cues, ensuring a fully synchronized viewing experience.

### Stage 3 — Video Production & Encoding
- Merges audio and visual streams into a single production-ready video file.
- Applies encoding standards suitable for YouTube's ingestion pipeline (H.264/AAC via `FFmpeg`).
- Performs quality validation before passing the asset downstream.

### Stage 4 — Automated YouTube Publishing
- Authenticates with the YouTube Data API v3 via OAuth 2.0.
- Programmatically constructs and injects metadata: title, description, tags, thumbnail, category, and privacy settings.
- Uploads the final video and confirms successful publication.
- Schedules the next cycle to trigger in **8 hours**, maintaining an uninterrupted content stream.

---

## 🛠 Technology Stack

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Core Language** | Python 3.10+ | Full pipeline orchestration and automation logic |
| **Audio Synthesis** | gTTS / Custom TTS | Whisper narration and voice generation |
| **Audio Processing** | Pydub / AudioSegment | Mixing, effects layering, stereo spatialization |
| **Video Production** | MoviePy | Audio-visual merging, frame rendering, clip composition |
| **Encoding** | FFmpeg (via Python wrappers) | High-quality encoding, format conversion, stream muxing |
| **Browser Automation** | Selenium | Fallback UI automation for steps outside API scope |
| **Platform Integration** | YouTube Data API v3 | Video upload, metadata injection, channel management |
| **Auth & Credentials** | Google Cloud / OAuth 2.0 | Secure, token-based API authentication |
| **Configuration** | YAML | Environment-specific settings, credentials references, scheduling params |

---

## ⚙️ Configuration & Setup

All runtime behavior is controlled through a central `config.yaml` file. This includes YouTube channel targeting, scheduling intervals, content generation parameters, and references to securely stored credentials.

> ⚠️ **No API keys or credentials are hardcoded anywhere in this codebase.** All sensitive values are loaded from environment variables or a `.env` file excluded from version control via `.gitignore`.
```yaml
# config.yaml (example structure — values omitted)
youtube:
  channel_id: YOUR_CHANNEL_ID
  default_privacy: public
  category_id: "22"

scheduling:
  interval_hours: 8

content:
  themes:
    - rainfall_ambient
    - soft_tapping
    - whisper_narrative
  audio_duration_seconds: 600

credentials:
  client_secrets_path: /path/to/client_secrets.json
  token_path: /path/to/token.json
```

---

## ⚠️ Important Notice — Service Discontinuation

The automated content generation and upload services operated by this system have been **permanently terminated**.

This decision was made in direct response to new regulations introduced by the **Indian Government** concerning the monetization of AI-generated video content on platforms such as YouTube. These regulatory changes materially impact the economic viability of automated AI content pipelines operating within India.

📎 Reference: [YouTube Monetisation Update — Economic Times](https://economictimes.indiatimes.com/news/new-updates/youtube-monetisation-update-today-who-will-be-affected-is-there-new-eligibility-requirement-whats-changing-heres-all/articleshow/122482003.cms?from=mdr)

This project adheres to all applicable local and international regulations. The codebase is preserved in its entirety as a **technical reference and educational resource**, demonstrating the architecture and implementation of a production-grade, end-to-end AI content automation system.

---

## 💡 What This Project Demonstrates

Beyond its original use case, this codebase serves as a working reference for:

- **Multi-stage pipeline architecture** in Python for content automation.
- **Audio engineering in Python** — mixing, layering, and spatializing sound programmatically.
- **YouTube Data API v3 integration** — authenticated uploads, metadata management, and channel automation.
- **Secure credential management** using Google Cloud and OAuth 2.0 flows.
- **Scheduler design** for long-running, self-healing automation processes.
- **FFmpeg integration** for production-quality media encoding from within a Python application.

---

## 📬 Connect & Collaborate

Open to discussions on automation engineering, AI content systems, and high-impact technical projects.

- **LinkedIn:** [linkedin.com/in/anusthan12](https://www.linkedin.com/in/anusthan12/)
- **Email:** [anusthan.singh12@gmail.com](mailto:anusthan.singh12@gmail.com)
- **Portfolio:** [anusthan-singh.vercel.app](https://anusthan-singh.vercel.app/)

---

<div align="center">
  <p>Built and maintained by <a href="https://github.com/anusthan12">Anusthan Singh</a> · © 2025</p>
</div>
