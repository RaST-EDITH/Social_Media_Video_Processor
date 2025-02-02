# Social Media Video Processor

A Python-based tool that transforms long videos into engaging short-form content suitable for social media platforms like Instagram Reels, YouTube Shorts, and TikTok.

## 🎯 Features

- Converts videos to 9:16 aspect ratio (vertical format)
- Adds smooth transitions between clips
- Overlays text with animations
- Mixes background music with original audio
- Detects and processes interesting segments
- Real-time preview of processing steps

## 🔧 Prerequisites

Before running this project, make sure you have:
- Python 3.8 or higher installed
- Pip (Python package installer)
- Basic understanding of command line operations

## 💻 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RaST-EDITH/Social_Media_Video_Processor.git
   cd Social_Media_Video_Processor
   ```

2. **Set up a virtual environment**
   
   For Windows:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   venv\Scripts\activate
   ```

   For macOS/Linux:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Upgrade pip
   python -m pip install --upgrade pip
   
   # Install required packages
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. **Prepare your input files**
   - Place your input video in the project directory
   - Prepare background music (MP3 format)
   - Identify interesting timestamps in your video

2. **Run the script**
   ```python
   from video_processor import VideoProcessorPureCV

   # Define timestamps for interesting clips
   clips_timestamps = [
       (5, 9),    # First clip: 5s to 9s
       (15, 20),  # Second clip: 15s to 20s
       (35, 40)   # Third clip: 35s to 40s
   ]

   # Initialize processor
   processor = VideoProcessorPureCV(
       input_video_path="your_video.mp4",
       output_path="output_short.mp4",
       clips_timestamps=clips_timestamps,
       music_path="your_music.mp3"
   )

   # Process video
   processor.process_video()
   ```

3. **Find your processed video**
   - The output video will be saved as specified in `output_path`
   - Default format is MP4, optimized for social media

## 📁 Project Structure

```
social-media-video-processor/
├── README.md
├── requirements.txt
├── video_processor.py
├── venv/
├── input/
│   ├── videos/
│   └── music/
└── output/
```

## ⚙️ Configuration Options

You can customize various aspects of the video processing:

```python
# Modify transition duration (in frames)
transition_frames = 30  # Default: 30 frames

# Adjust text overlay duration
text_duration = 60  # Default: 60 frames (2 seconds at 30fps)

# Change text style
font_scale = 1.0  # Text size
thickness = 2    # Text thickness
```

## 🔍 Troubleshooting

Common issues and solutions:

1. **Import errors after installation**
   ```bash
   # Try reinstalling dependencies
   pip uninstall -r requirements.txt
   pip install -r requirements.txt
   ```

2. **Video output quality issues**
   - Ensure input video is high quality
   - Check available disk space
   - Try adjusting the output codec settings

3. **Performance issues**
   - Close other resource-intensive applications
   - Reduce the number of transitions
   - Process shorter video segments


## 📝 Notes

- The processor works best with high-quality input videos
- Recommended video length: 30-60 seconds
- Supported input formats: MP4, AVI, MOV
- Supported audio formats: MP3, WAV
