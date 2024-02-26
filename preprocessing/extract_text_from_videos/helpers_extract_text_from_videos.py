from moviepy.editor import VideoFileClip
import whisper
import os

def extract_audio_from_video(video_path, output_audio_path):
    """
    Extracts the audio from a video file and saves it as an audio file.

    Parameters:
    video_path (str): Path to the video file.
    output_audio_path (str): Path where the extracted audio file will be saved.
    """
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_audio_path, codec='pcm_s16le')

def transcribe_audio_to_text(audio_path):
    """
    Transcribes the speech in an audio file to text using Whisper.

    Parameters:
    audio_path (str): Path to the audio file to transcribe.

    Returns:
    str: The transcribed text.
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

# Main pipeline function
def video_to_text_pipeline(video_path):
    """
    Processes a video file through the pipeline to extract audio and transcribe it to text.

    Parameters:
    video_path (str): Path to the video file.
    """
    audio_path = os.path.splitext(video_path)[0] + '.wav'
    
    extract_audio_from_video(video_path, audio_path)
    
    text = transcribe_audio_to_text(audio_path)
    
    os.remove(audio_path)
    
    return text
