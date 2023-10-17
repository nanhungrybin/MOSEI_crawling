import os
import cv2

import numpy as np

import pandas as pd
import logging
from queue import Queue

# 로그 설정
log_filename = '10-17_log.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


vid_error = []

# 프레임 간의 최대 차이를 설정
# max_frame_diff 개의 이전 프레임만 비교하도록
max_frame_diff = 53 #15

#check FPS
#24, 30, 60, 또는 120 FPS


# # check FPS

# import cv2
# import os
# import numpy as np


# video_directory = '/home/face/Desktop/hb/cv_new/redown_mosei/segment_videos'
# fpss = []
# for filename in os.listdir(video_directory):
#     if filename.endswith('.mp4'):
#         video_path = os.path.join(video_directory, filename)
#         cap = cv2.VideoCapture(video_path)
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         print(f"동영상 {filename}의 FPS: {fps}")
#         fpss.append(fps)
#         cap.release()
# print(np.mean(fpss))




# 디렉토리 경로 설정
directory_path = '/home/face/Desktop/hb/cv_new/redown_mosei/segment_videos'


# 디렉토리 내의 파일 목록 읽기
video_files = [f for f in os.listdir(directory_path)]

for video_file in video_files:
    video_file_path = os.path.join(directory_path, video_file)


    # VideoCapture를 사용하여 동영상 파일 열기
    cap = cv2.VideoCapture(video_file_path)

    ######## 이전 max_frame_diff개의 프레임을 저장 위한 QUEUE #######
    prev_frames = Queue()


    no_face_ranges = []  # List to store the ranges of frames without faces
    start_frame = None  # Initialize the start frame variable
    
    # 각 frame별 동영상 처리 코드 추가
    while True:
        ret, frame = cap.read()
        
        # video reading error
        read_error = []

        if not ret: #False
            read_error.append(video_file_path)

            if cap.get(cv2.CAP_PROP_FRAME_COUNT) > 0: #for division error

                if read_error and len(read_error) / cap.get(cv2.CAP_PROP_FRAME_COUNT) > 0.5: #because one of video after 148 frame error


                # 예외처리: "mmco: unref short failure" 에러가 발생할 때만 해당 동영상 파일을 vid_error 리스트에 추가
                    if "mmco: unref short failure" in str(cap.get(cv2.CAP_PROP_POS_FRAMES)):
                        # 터미널 출력 내용을 로그 파일에도 기록
                        logging.error(f"Error reading video: {video_file_path}")
                        print(f"Error reading video: {video_file_path}")
                        vid_error.append(video_file_path)
                    else:
                        # 터미널 출력 내용을 로그 파일에도 기록
                        logging.error(f"Error reading video: {video_file_path}")
                        print(f"Error reading video: {video_file_path}")
                        vid_error.append(video_file_path)

            elif cap.get(cv2.CAP_PROP_FRAME_COUNT) == 0:

                if "mmco: unref short failure" in str(cap.get(cv2.CAP_PROP_POS_FRAMES)):
                        # 터미널 출력 내용을 로그 파일에도 기록
                        logging.error(f"Error reading video: {video_file_path}")
                        print(f"Error reading video: {video_file_path}")
                        vid_error.append(video_file_path)
                else:
                    # 터미널 출력 내용을 로그 파일에도 기록
                    logging.error(f"Error reading video: {video_file_path}")
                    print(f"Error reading video: {video_file_path}")
                    vid_error.append(video_file_path)


            break


        # 10프레임 사이 반복되는 영상 찾기

        # 이전 프레임을 큐에 추가
        # prev_frames.append(frame.copy())
        # 현재 프레임 추가
        prev_frames.put(frame)


        # 큐의 길이가 max_frame_diff를 초과하면 가장 오래된 프레임을 제거
        if prev_frames.qsize() > max_frame_diff:
            prev_frames.get()

        if prev_frames.qsize() == max_frame_diff:
            frames_equal = all(np.array_equal(prev_frames.queue[0], prev_frames.queue[i]) for i in range(1, max_frame_diff))
            
            if frames_equal:
                # 10 프레임이 모두 동일하면 반복된 것으로 간주
                print(f"Frame freeze detected in video: {video_file_path}")
                vid_error.append(video_file_path)
                #read_error.append(video_file)
                logging.error(f"Frame freeze detected in video: {video_file_path}")

                break


            


        
        
    # 사용한 자원 해제
    cap.release()

# 로그 파일 닫기
logging.shutdown()


print(len(read_error))

#real
print(len(vid_error))



# 리스트를 DataFrame으로 변환
df = pd.DataFrame({'Video Name': vid_error})

# DataFrame을 CSV 파일로 저장
df.to_csv('re_vid_error.csv', index=False)