import cv2
import os
import json

from preprocess import *
from secs_to_time import secs_to_timestr
from time_segment import *
import yt_dlp
import pandas as pd

# def download(video_pasth, ytb_id, proxy=None):
#     """
#     ytb_id: youtube_id
#     save_folder: save video folder
#     proxy: proxy url, defalut None
#     """
#     if proxy is not None:
#         proxy_cmd = "--proxy {}".format(proxy)
#     else:
#         proxy_cmd = ""
        
#     if not os.path.exists(video_path):
#         down_video = " ".join([
#             "yt-dlp",
#             proxy_cmd,
#             '-f', "'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio'",
#             '--skip-unavailable-fragments',
#             '--merge-output-format', 'mp4',
#             "https://www.youtube.com/watch?v=" + ytb_id, "--output",
#             video_path, "--external-downloader", "aria2c",
#             "--external-downloader-args", '"-x 16 -k 1M"',
#             "--download-sections", '0:09-4:29',
#         ])
       
#         status = os.system(down_video)
#         if status != 0:
#             print(f"video not found: {ytb_id}")


def load_data(file_path):
    with open(file_path) as f:
        data_dict = json.load(f)

    for key, val in data_dict['clips'].items():
        save_name = key+".mp4"
        ytb_id = val['ytb_id']
        time = val['duration']['start_sec'], val['duration']['end_sec']

        bbox = [val['bbox']['top'], val['bbox']['bottom'],
                val['bbox']['left'], val['bbox']['right']]
        yield ytb_id, save_name, time, bbox



# def main():
#     # CSV 파일 경로 설정
#     csv_file_path = 'mosei.csv'
    
#     # CSV 파일 읽기
#     df = pd.read_csv(csv_file_path)

#     # "id", "start", "end" 열의 값 가져오기
#     #ids = df['id']
#     ids = df['link'].str[-11:]
#     start_times = df['start']
#     end_times = df['end']
    
#     vid_root = "/home/face/Desktop/cv_new/videos"
#     proxy = None  # proxy url example, set to None if not use

#     os.makedirs(vid_root, exist_ok=True)
    
#     for i in range(len(ids)):
#         # 각 데이터를 가져옴
#         ytb_id = ids[i]
#         start_time = start_times[i]
#         end_time = end_times[i]
#         start_sec = secs_to_timestr(start_time)
#         end_sec = secs_to_timestr(end_time)

#         # 시간 범위 설정 문자열 생성
#         time_range = f"*{start_sec}-{end_sec}"

#         # 원하는 시간 범위로 추출한 YouTube 동영상 다운로드
#         vid_path = os.path.join(vid_root, f"{ytb_id}.mp4")
        
        
        
#         #ytb_url = f'https://www.youtube.com/watch?v={ytb_id}'
#         ydl_opts = {
#         'format': 'best[ext=mp4]/best',
#         'outtmpl': vid_path,
#         'quiet': True,
#              }
    
#         try:
#             #with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             #    ydl.download([ytb_url])
#             download(vid_path, ytb_id, time_range, proxy)
#         except yt_dlp.utils.DownloadError as e:
#             print(f"Error downloading video with ID {ytb_id}: {str(e)}")


# 비디오 ID의 유효성을 확인하는 함수
def check_valid_ytb_id(ytb_id):
    return len(ytb_id) == 11

def main():
    # CSV 파일 경로 설정
    csv_file_path = 'test.csv'

    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path)

    # Create DataFrame for saving downloaded video info. 
    dl_csv = pd.DataFrame(columns=list(df.columns))

    # "id", "seg_id", "start", "end" 열의 값 가져오기
    ids = df['link'].str.split('=')  # = 기준으로 문자열 분리
    ids = ids.str[-1]  # 분리된 문자열 중 마지막 부분 선택
    segs = df['segment_id']
    start_times = df['start']
    end_times = df['end']

    assert len(ids) == len(segs)  # Check if equal. 

    vid_root = "/home/face/Desktop/cv_new/test_videos"
    proxy = None  # proxy url example, set to None if not use

    os.makedirs(vid_root, exist_ok=True)

    processed_ids = []

    for i in range(len(ids)):
        # 각 데이터를 가져옴
        ytb_id = ids[i]
        seg_id = segs[i]

        # 비디오 ID의 유효성을 확인
        if not check_valid_ytb_id(ytb_id):
            print(f"Invalid video ID: {ytb_id}")
            continue  # 유효하지 않은 경우 스킵

        start_time = start_times[i]
        end_time = end_times[i]
        start_sec = secs_to_timestr(start_time)
        end_sec = secs_to_timestr(end_time)

        # 시간 범위 설정 문자열 생성
        time_range = f"*{start_sec}-{end_sec}"

        # 원하는 시간 범위로 추출한 YouTube 동영상 다운로드
        vid_path = os.path.join(vid_root, f"{ytb_id}_{seg_id}.mp4")

        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': vid_path,
            'quiet': True,
        }

        try:
            download(vid_path, ytb_id, time_range, processed_ids, proxy)  
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading video with ID {ytb_id}_{seg_id}: {str(e)}")

        # If video was downloaded, add information to new csv. 
        if os.path.exists(vid_path):
            row = df.iloc[[i]]
            row["id"].values[0] += f"_{seg_id}"
            dl_csv = pd.concat([dl_csv, row])     
            print('Info stored in CSV!')
                
    dl_csv.to_csv('kist_mosei.csv', index=False)

if __name__ == "__main__":
    main()
