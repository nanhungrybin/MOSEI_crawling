import pandas as pd
import os
import yt_dlp

# CSV 파일 경로 설정
csv_file_path = "/home/face/Desktop/hb/cv_new/redown_mosei/vid_error_link.csv"   # CSV 파일 경로를 수정하세요

# CSV 파일 읽기
df = pd.read_csv(csv_file_path)

# 동영상을 저장할 디렉토리 생성
output_dir = "/home/face/Desktop/hb/cv_new/redown_mosei/re_videos"
os.makedirs(output_dir, exist_ok=True)

# YouTube 동영상 다운로드 함수 정의
def download_youtube_video(ytb_id, youtube_url, output_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

# YouTube 동영상 다운로드
for index, row in df.iterrows():
    ytb_id = row['id']
    youtube_url = row['link']
    output_path = os.path.join(output_dir, f"{ytb_id}.mp4")

    if not os.path.exists(output_path):
        try:
            download_youtube_video(ytb_id, youtube_url, output_path)
            print(f"Downloaded: {ytb_id}")
        except Exception as e:
            print(f"Error downloading {ytb_id}: {str(e)}")
    else:
        print(f"Already downloaded: {ytb_id}")