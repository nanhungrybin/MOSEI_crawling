import yt_dlp
import os

""" yt-dlp hls issue: https://www.reddit.com/r/youtubedl/wiki/h264/#wiki_download_h264 """

def download(video_path, ytb_id, time_range, processed_ids, proxy=None):

    if proxy is not None:
        proxy_cmd = "--proxy {}".format(proxy)
    else:
        proxy_cmd = ""
    if not os.path.exists(video_path):
        # 추가 인수와 인수 이름을 명시적으로 설정
        aria2c_args = "aria2c:-x 16 -k 1M"
        down_video = " ".join([
            "yt-dlp",
            proxy_cmd,
            '-f', "'bestvideo[ext=mp4][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo+bestaudio'",
            '--skip-unavailable-fragments',
            '--merge-output-format', 'mp4',
            "--download-sections", time_range,
            "https://www.youtube.com/watch?v=" + ytb_id, "--output",
            video_path, "--external-downloader", "aria2c",
            "--external-downloader-args", f'"{aria2c_args}"', 
            "--verbose", "2>&1 | tee output.log" 
        ])
        
        print(down_video)
        print(time_range)
        status = os.system(down_video)

        # Log errors. 
        with open('output.log') as f: 
            f = f.readlines()
            
            for line in f:
                # if 'ERROR:' in line:
                if line.startswith('ERROR: [youtube]'):
                    video_id = line.split('ERROR: [youtube] ')[1].split(':')[0]
                    
                    # 이미 처리한 id라면 건너뛰기
                    if video_id in processed_ids:
                        break
                    
                    processed_ids.append(video_id)
                    txt_file = open("error.txt", "a")
                    txt_file.write(line)
                    txt_file.close()
                     

        if status != 0:
            print(f"video not found: {ytb_id}")
        