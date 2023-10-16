import pandas as pd
import os
from pytube import YouTube

# CSV 파일 경로 설정
csv_file_path = "/home/face/Desktop/hb/cv_new/redown_mosei/vid_error_link.csv"  # CSV 파일 경로

# CSV 파일 읽기
df = pd.read_csv(csv_file_path)

# 동영상을 저장할 디렉토리 생성
output_dir = "/home/face/Desktop/hb/cv_new/redown_mosei/re_videos"
os.makedirs(output_dir, exist_ok=True)



def download_youtube_video(youtube_url, output_dir, ytb_id):
    yt = YouTube(youtube_url)
    stream = yt.streams.get_highest_resolution()
    
    # 파일 이름을 ytb_id로 설정
    output_path = os.path.join(output_dir, f"{ytb_id}.mp4")

    if not os.path.exists(output_path):
        try:
            stream.download(output_path)
            print(f"Downloaded: {ytb_id}")


        except Exception as e:
            print(f"Error downloading {ytb_id}: {str(e)}")
    else:
        print(f"Already downloaded: {ytb_id}")



# YouTube 동영상 다운로드
for index, row in df.iterrows():
    ytb_id = row['id']
    youtube_url = row['link']

    if not os.path.exists(os.path.join(output_dir, f"{ytb_id}.mp4")):
        try:
            download_youtube_video(youtube_url, output_dir, ytb_id)
        except Exception as e:
            print(f"Error downloading {ytb_id}: {str(e)}")
    else:
        print(f"Already downloaded: {ytb_id}")