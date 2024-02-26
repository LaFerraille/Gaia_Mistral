from datasets import load_dataset
from .helpers_extract_text_from_videos import video_to_text_pipeline

dataset = load_dataset("HuggingFaceM4/howto100m", split='train')
output_directory = "data/videos/test" 
video_path = "data/videos/"
text = video_to_text_pipeline(video_path)
print(text)