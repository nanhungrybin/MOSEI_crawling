# MOSEI_crawling

#### 감정인식을 위한 CMU Multimodal Opinion Sentiment and Emotion Intensity (CMU-MOSEI) 데이터셋을 구축하기 위한 코드

CMU Multimodal Opinion Sentiment and Emotion Intensity (CMU-MOSEI) is the largest dataset of sentence level sentiment analysis and emotion recognition in online videos. CMU-MOSEI contains more than 65 hours of annotated video from more than 1000 speakers and 250 topics. http://multicomp.cs.cmu.edu/resources/cmu-mosei-dataset/
![image](https://github.com/nanhungrybin/MOSEI_crawling/assets/97181397/3d0eaee0-fb5f-4d5e-9bcd-5051634765c0)



### 📁 수집 과정에서 발생한 문제 📁

#### 첫번째 발생 문제 : 선 수집후 동영상을 원하는 시간으로 자르면 다운로드의 시간이 30일 정도 걸림

- 처음부터 감정을 나타내는 시간 포인트에 해당되는 부분만 다운로드 할 수 있게 하자
![image](https://github.com/nanhungrybin/MOSEI_crawling/assets/97181397/b73a10df-a1d4-40de-9232-ca0883770e42)


#### 두번째 발생 문제 : 23259개의 동영상 중 총 2264개만 수집됨

- 동일한 영상이지만 다른 segment인 영상 => 중복 id 존재
- 존재하지 않는 동영상/ 비공개 동영상 X => 중복된 영상 id를 갖고 있는 문제된 몇개의 동영상의 영향
- 다운로드 되지 않는 영상 => 로그파일을 형성, 이들 중 미중복 id만 추출하는 error text파일 형성
- 564개의 오류 동영상 확인, 2종류의 오류문 발견 ( private video / video unavailable )

#### 세번째 발생 문제 : 13205개 다운로드 후 영상 재생이 안되는 동영상 발생

- 동영상을 다운로드 받는 과정에서 스트리밍 동영상과 같은 포멧 차이
- hls형식인 비디오 스트림 다운로드를 위한 H.264 비디오 코덱 사용 코드 추가
![image](https://github.com/nanhungrybin/MOSEI_crawling/assets/97181397/07c28b87-59c1-4cfe-887f-5bb45316a3e2)

#### 네번째 발생 문제 :

- 사람 얼굴이 없는 동영상 ▶ RetinaFace face detect

- Frame freeze 영상 ▶ Frame freeze detect

- 비디오 리더기 에러 및 손상된 파일 ▶  detect



#1. Frame freeze 영상 / 비디오 리더기 에러 및 손상된 파일

- ID 검출

- 세그먼트 별이 아닌 전체 영상 다운로드 후 파싱


#2. 사람 얼굴이 없는 동영상 

- Face Detecter Model인 RETINAFACE를 사용해 검출 [https://github.com/nanhungrybin/](https://github.com/nanhungrybin/Retinaface_torch)

- 전체 프레임 중 얼굴이 등장하지 않는 비율 검출

- 얼굴이 등장하지 않는 프레임 범위 검출 ▶ 추후 해당 프레임 제거한 후 dataset으로 사용 가능 / No Face 기준 논의 가능


## 📁 WHAT IS MOSEI 📁
![image](https://github.com/nanhungrybin/MOSEI_crawling/assets/97181397/c68f72c2-7292-46d0-b056-6bef5089eee7)

## 📁 WHY MOSEI 📁 왜 MOSEI는 중요한가? 왜 직접 수집해야하는가 ?



