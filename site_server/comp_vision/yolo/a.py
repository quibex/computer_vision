import os

output_file_name = "short.mp4"
transcoded_video = "short_transcoded.mp4"
os.system(f"ffmpeg -y -i {output_file_name} -vcodec libx264 {transcoded_video}")