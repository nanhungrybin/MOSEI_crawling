import cv2
import os
import json

from all_download import download
import yt_dlp
import pandas as pd


def load_data(file_path):
    with open(file_path) as f:
        data_dict = json.load(f)

    for key, val in data_dict['clips'].items():
        save_name = key+".mp4"
        ytb_id = val['ytb_id']
        
        bbox = [val['bbox']['top'], val['bbox']['bottom'],
                val['bbox']['left'], val['bbox']['right']]
        yield ytb_id, save_name, bbox


# 비디오 ID의 유효성을 확인하는 함수
def check_valid_ytb_id(ytb_id):
    return len(ytb_id) == 11


def main(csv_file_path, vid_root):

    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path)

    # Create DataFrame for saving downloaded video info. 
    dl_csv = pd.DataFrame(columns=list(df.columns))

    # "id"값 가져오기
    ids = df['id']
    proxy = None  # proxy url example, set to None if not use

    os.makedirs(vid_root, exist_ok=True)

    processed_ids = []

    for i in range(len(ids)):
        # 각 데이터를 가져옴
        ytb_id = df['id']
    
        # 비디오 ID의 유효성을 확인
        if not check_valid_ytb_id(ytb_id):
            print(f"Invalid video ID: {ytb_id}")
            continue  # 유효하지 않은 경우 스킵


        # YouTube 동영상 다운로드
        vid_path = os.path.join(vid_root, f"{ytb_id}.mp4")

        try:
            download(vid_path, ytb_id, processed_ids, proxy)  
            print("done")
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading video with ID {ytb_id}: {str(e)}")

        # If video was downloaded, add information to new csv. 
        if os.path.exists(vid_path):
            row = df.iloc[[i]]
            dl_csv = pd.concat([dl_csv, row])     
            print('Info stored in CSV!')
    
    dl_csv.to_csv('redown_mosei.csv', index=False)


if __name__ == "__main__":
    
    # CSV 파일 경로 설정
    csv_file_path = "/home/face/Desktop/hb/cv_new/redown_mosei/vid_error_link.csv"
    
    # Output video path.  
    vid_root = "/home/face/Desktop/hb/cv_new/redown_mosei/re_videos"

    # Run. 
    main(csv_file_path, vid_root)