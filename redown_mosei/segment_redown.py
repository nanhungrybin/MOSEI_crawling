
import os
import cv2
import pandas as pd

def segment(start_time, end_time, input_file, output_root):


    # 동영상 로드
    cap = cv2.VideoCapture(input_file)

    # 동영상 정보 가져오기
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 출력 동영상 설정
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 동영상 코덱 설정 (MP4 포맷)
    out = cv2.VideoWriter(output_root, fourcc, frame_rate, (frame_width, frame_height))

    # 시작 시간까지 동영상을 읽어서 버리기
    while cap.get(cv2.CAP_PROP_POS_MSEC) < start_time * 1000:
        _, frame = cap.read()
        

    # 시작 시간부터 종료 시간까지 프레임을 읽어서 출력 동영상에 쓰기
    while cap.get(cv2.CAP_PROP_POS_MSEC) < end_time * 1000:   #밀리초로 변환하기 위해 1000을 곱
        _, frame = cap.read()
        out.write(frame)
     

    # 사용한 리소스 해제
    cap.release()
    out.release()
    cv2.destroyAllWindows()

   



def main(csv_file_path, input_root, output_root):

    df = pd.read_csv(csv_file_path)
    
    for i in range(len(df)):
        start_time = df["start"][i]
        end_time = df["end"][i]

        input_id = df["id"][i] # 파싱할 동영상 파일 
        segment_id = df['segment_id'][i]#파싱할 동영상 세그먼트 id

        # 올바른 입력 파일 경로 생성
        input = os.path.join(input_root, f"{input_id}.mp4")

        # 올바른 출력 파일 경로 생성
        output_filename = f"{input_id}_{segment_id}.mp4" 
        output = os.path.join(output_root, output_filename)


        # 이미 동영상 파일이 존재하면 넘어감
        if os.path.exists(output):
            print(f"Video already exists: {output_filename}")
            continue

        try:
            segment(start_time, end_time, input, output)
            print(f"Segmentation done: {output_filename}")
        except Exception as e:
            print(f"Error processing video: {output_filename}, Error: {str(e)}")



if __name__ == "__main__":

    csv_file_path = "/home/face/Desktop/hb/cv_new/redown_mosei/filtered_mosei_segment.csv"

    input_root = "/home/face/Desktop/hb/cv_new/redown_mosei/re_videos"

    output_root = "/home/face/Desktop/hb/cv_new/redown_mosei/segment_videos"

    main(csv_file_path, input_root, output_root)

    





