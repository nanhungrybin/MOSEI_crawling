import cv2
import os
import json

from preprocess import secs_to_timestr
from download import download
import yt_dlp
import pandas as pd


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


# 비디오 ID의 유효성을 확인하는 함수
def check_valid_ytb_id(ytb_id):
    return len(ytb_id) == 11


def main(csv_file_path, vid_root):

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
    
    # CSV 파일 경로 설정
    csv_file_path = '/home/face/Desktop/hb/cv_new/mosei/mosei.csv'
    
    # Output video path.  
    vid_root = "/home/face/Desktop/hb/cv_new/videos"

    # Run. 
    main(csv_file_path, vid_root)
