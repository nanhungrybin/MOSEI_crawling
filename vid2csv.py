import csv
import os

# 비디오 파일이 들어 있는 디렉토리 경로
video_dir = 'videos'

# 비디오 파일 목록 수집
video_files = sorted(os.listdir(video_dir))

# CSV 파일 경로
csv_file = 'video_list.csv'

# CSV 파일 작성
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # CSV 파일 헤더 작성 (예: "Video ID,Video URL")
    writer.writerow(['id', 'link'])
    
    # 비디오 파일 목록을 기반으로 각 비디오에 대한 정보 작성
    for video_file in video_files:
        video_id = os.path.splitext(video_file)[0]  # 파일 이름에서 확장자 제거하여 Video ID 추출
        video_url = f'https://www.youtube.com/watch?v={video_id}'  # 비디오 URL 생성
        writer.writerow([video_id, video_url])

print(f'CSV 파일이 생성되었습니다: {csv_file}')