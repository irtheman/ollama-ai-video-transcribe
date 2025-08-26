#!/usr/bin/env -S python3


import sys
from moviepy import VideoFileClip

def convert_video_to_audio(video_path, audio_path):
    """ Converts an mp4 video file to an m4a audio file using moviepy. """
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path, codec="aac")
        audio_clip.close()
        video_clip.close()
        print(f"Successfully converted '{video_path}' to '{audio_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Invalid number of arguments. Usage: python video-to-audio.py <video_file.mp4> <audio_file.m4a>")
        sys.exit(1)
    
    video_file_path = sys.argv[1]
    audio_file_path = sys.argv[2]

    try:
        convert_video_to_audio(video_file_path, audio_file_path)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
