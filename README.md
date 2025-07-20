🎧 Automated ASMR Content Creator & YouTube Uploader 🎥
Note: This project's services have been discontinued due to recent changes in Indian government regulations regarding the monetization of AI-generated video content on platforms like YouTube. For more details, please refer to this article: https://economictimes.indiatimes.com/news/new-updates/youtube-monetisation-update-today-who-will-be-affected-is-there-new-eligibility-requirement-whats-changing-heres-all/articleshow/122482003.cms?from=mdr

This repository houses the code for an innovative, fully end-to-end automated chatbot designed to generate unique ASMR (Autonomous Sensory Meridian Response) video and audio content, and then seamlessly upload it to YouTube on a regular 8-hour schedule. The goal was to create a self-sustaining content pipeline, from concept to publication, without manual intervention.

✨ Project Overview & End-to-End Automation
Our ASMR Video Generation Chatbot was engineered for complete autonomy. The workflow was meticulously designed to handle every step of content creation and distribution:

ASMR Content Generation:

The chatbot would interpret user prompts or pre-defined themes to conceptualize ASMR scenarios.

It would then generate ASMR audio tracks using a combination of text-to-speech (TTS) for whispered narratives and synthesized ambient sounds/effects (e.g., tapping, crinkling, gentle rain) to create immersive soundscapes.

Concurrently, visual elements (e.g., abstract animations, calming patterns, simple object movements) would be generated or selected to complement the audio, creating a synchronized ASMR video.

Video & Audio Production Pipeline:

The generated audio and visual components were then programmatically merged and processed to form a complete video file. This involved precise synchronization and encoding to ensure high-quality output suitable for YouTube.

Automated YouTube Upload:

Once a video was finalized, the system would automatically handle the upload process to a designated YouTube channel. This included setting video titles, descriptions, tags, and privacy settings.

Scheduled Publication:

A robust scheduling mechanism ensured that a new ASMR video was generated and uploaded every 8 hours, maintaining a consistent content flow without requiring manual oversight.

🛠️ Technologies Used
This project leveraged a stack of powerful tools and libraries to achieve its automation goals:

Python: The core programming language for the entire system, orchestrating all generation, processing, and automation tasks.

Automation Libraries:

gTTS (Google Text-to-Speech) or similar for generating natural-sounding whispered audio.

Pydub or AudioSegment for audio manipulation, mixing, and applying effects.

MoviePy or similar for video editing, combining audio and visual elements, and rendering final video files.

Selenium (or similar browser automation tools) for interacting with web interfaces, if direct API access was insufficient for certain steps.

FFmpeg (via Python wrappers) for powerful video and audio encoding/decoding and format conversions.

YAML: Used for configuration management, storing settings such as YouTube channel details, API keys (securely referenced, not hardcoded), content generation parameters, and scheduling preferences.

Google YouTube Data API: Essential for programmatically uploading videos, managing video metadata (titles, descriptions, tags), and interacting with the YouTube platform. Secure authentication was handled via OAuth 2.0.

Google Cloud Credentials: Securely managed API keys and service account credentials for accessing Google services, including YouTube.

⚠️ Important Note: Service Discontinuation
As mentioned above, the automated content generation and upload services provided by this project have been terminated. This decision was made in direct response to new regulations introduced by the Indian government concerning the monetization of AI-generated video content. These changes significantly impact the economic viability of such automated systems on platforms like YouTube within India.

We believe in adhering to all local and international regulations, and as such, the operational aspect of this project has been ceased. The codebase remains here for educational and reference purposes, showcasing the technical capabilities of end-to-end AI content automation.
