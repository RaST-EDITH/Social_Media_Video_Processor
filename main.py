import cv2
import numpy as np
import moviepy.editor as mp
from moviepy.audio.AudioClip import CompositeAudioClip
from tqdm import tqdm
import os

class VideoProcessorCV:
    def __init__(self, input_video_path, output_path, clips_timestamps, music_path):
        """
        Initialize video processor with OpenCV
        """
        self.input_path = input_video_path
        self.output_path = output_path
        self.clips_timestamps = clips_timestamps
        self.music_path = music_path
        self.target_ratio = 9/16
        self.fps = 30
        
    def add_text_opencv(self, frame, text, position=None, font_scale=1, thickness=2):
        """Add text to frame using OpenCV"""
        height, width = frame.shape[:2]
        
        # If position not specified, put text at bottom center
        if position is None:
            position = (width // 2, height - 50)
            
        # Font settings
        font = cv2.FONT_HERSHEY_DUPLEX
        
        # Get text size
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        
        # Center text
        x = position[0] - text_width // 2
        y = position[1]
        
        # Add black outline (shadow)
        cv2.putText(frame, text, (x, y), font, font_scale, (0, 0, 0), thickness + 2)
        # Add white text
        cv2.putText(frame, text, (x, y), font, font_scale, (255, 255, 255), thickness)
        
        return frame

    def create_transition(self, frame1, frame2, progress):
        """Create fade transition between frames"""
        return cv2.addWeighted(frame1, 1 - progress, frame2, progress, 0)

    def crop_to_vertical(self, frame):
        """Crop frame to 9:16 aspect ratio"""
        height, width = frame.shape[:2]
        target_width = int(height * self.target_ratio)
        
        # Crop from center
        start_x = (width - target_width) // 2
        return frame[:, start_x:start_x + target_width]

    def process_video(self):
        """Process the video with OpenCV and add music with moviepy"""
        try:
            # Create temporary file for video without audio
            temp_output = "temp_output.mp4"
            
            clips_frames = []
            transition_frames = 30  # Number of frames for transition
            
            # Process each clip
            for start_time, end_time in self.clips_timestamps:
                cap = cv2.VideoCapture(self.input_path)
                
                # Set starting position
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_time * self.fps))
                
                # Read frames until end time
                frames = []
                while cap.get(cv2.CAP_PROP_POS_FRAMES) < end_time * self.fps:
                    ret, frame = cap.read()
                    if not ret:
                        break
                        
                    # Crop to vertical
                    frame = self.crop_to_vertical(frame)
                    frames.append(frame)
                
                cap.release()
                clips_frames.append(frames)
            
            # Setup video writer
            if not clips_frames:
                raise ValueError("No frames were processed")
                
            frame_height, frame_width = clips_frames[0][0].shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_output, fourcc, self.fps, (frame_width, frame_height))
            
            # Write frames with transitions
            for clip_idx, clip in enumerate(clips_frames):
                # Add text for this clip
                text = f"Part {clip_idx + 1}"
                
                # Process frames
                for frame_idx, frame in enumerate(clip):
                    # Add text at the start of each clip
                    if frame_idx < 60:  # Show text for 2 seconds
                        frame = frame.copy()  # Create copy to avoid modifying original
                        frame = self.add_text_opencv(frame, text)
                    
                    # Add transition if not last clip
                    if clip_idx < len(clips_frames) - 1 and frame_idx >= len(clip) - transition_frames:
                        next_clip = clips_frames[clip_idx + 1]
                        progress = (frame_idx - (len(clip) - transition_frames)) / transition_frames
                        frame = self.create_transition(frame, next_clip[0], progress)
                    
                    out.write(frame)
            
            out.release()
            
            # Add music using moviepy
            print("Adding music...")
            video = mp.VideoFileClip(temp_output)
            audio = mp.AudioFileClip(self.music_path)
            
            # Loop or trim audio to match video length
            if audio.duration > video.duration:
                audio = audio.subclip(0, video.duration)
            else:
                audio = audio.loop(duration=video.duration)
            
            # Set audio volume
            audio = audio.volumex(0.7)
            
            # Combine video with music
            final_video = video.set_audio(audio)
            final_video.write_videofile(
                self.output_path,
                codec='libx264',
                audio_codec='aac'
            )
            
            # Cleanup
            video.close()
            audio.close()
            if os.path.exists(temp_output):
                os.remove(temp_output)
                
            print(f"Video successfully processed and saved to {self.output_path}")
            
        except Exception as e:
            print(f"Error processing video: {str(e)}")
            raise
        
if __name__ == "__main__":
    clips_timestamps = [
        (5, 9),    # First interesting clip
        (15, 20),  # Second interesting clip
        (35, 40)   # Third interesting clip
    ]
    
    processor = VideoProcessorCV(
        input_video_path=r"D:\fog\sample.mp4",
        output_path="output_short.mp4",
        clips_timestamps=clips_timestamps,
        music_path=r"D:\fog\friday.mp3"
    )
    
    processor.process_video()