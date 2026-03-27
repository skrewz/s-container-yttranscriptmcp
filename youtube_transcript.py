#!/usr/bin/env python3
"""YouTube Transcript Extractor"""

from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url_or_id):
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    patterns = [r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]{11})']
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Invalid YouTube URL or ID: {url_or_id}")


def get_transcript(video_id_or_url):
    video_id = extract_video_id(video_id_or_url)
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    transcript = transcript_list.find_transcript(['en'])
    return transcript.fetch()


if __name__ == '__main__':
    video_id = "YpPcDHc3e9U"
    
    print(f"Fetching transcript for video ID: {video_id}")
    print("-" * 40)
    
    try:
        transcript = get_transcript(video_id)
        print("Transcript fetched successfully!")
        print("-" * 40)
        
        full_text = ' '.join(segment.text for segment in transcript)
        print(full_text)
        
        output_file = "transcript.txt"
        with open(output_file, 'w') as f:
            f.write(full_text)
        print("-" * 40)
        print(f"Transcript saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
