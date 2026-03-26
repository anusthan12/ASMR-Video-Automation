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

<div align="center">
  <p>Built and maintained by <a href="https://github.com/anusthan12">Anusthan Singh</a> · © 2025</p>
</div>

> ⚠️ **No API keys or credentials are hardcoded anywhere in this codebase.** All sensitive values are loaded from environment variables or a `.env` file excluded from version control via `.gitignore`.
```yaml


