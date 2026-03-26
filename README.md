graph TD
    %% Node Definitions
    Trigger([8-Hour Chron Trigger]) --> Concept[Theme Conceptualization Engine]
    
    subgraph Synthesis_Layer [Content Synthesis & Rendering]
        Concept --> AudioGen[Neural TTS & Whisper Synthesis]
        Concept --> VisualGen[Procedural Visual Generation]
        AudioGen --> AudioMix[Pydub: Multi-track Binaural Layering]
        VisualGen --> Render[MoviePy/FFmpeg: Video Encoding]
        AudioMix --> Render
    end

    subgraph Distribution_Layer [Automated Deployment]
        Render --> Metadata[Dynamic SEO & Metadata Generator]
        Metadata --> Auth[OAuth 2.0 / YouTube API v3]
        Auth --> Upload[Headless YouTube Uploader]
    end

    Upload --> Registry[(Log Execution & Status)]
    Registry --> Success{Deployment Success?}
    Success -- Yes --> Standby([System Idle/Standby])
    Success -- No --> Retry[Error Handling & Logic Recovery]
    Retry --> Auth

    %% Styling
    style Synthesis_Layer fill:#f9f9f9,stroke:#333,stroke-width:2px
    style Distribution_Layer fill:#f0f4ff,stroke:#0055ff,stroke-width:2px
    style Trigger fill:#fff4dd,stroke:#d4a017
