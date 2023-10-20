# MOSEI_crawling

감정인식을 위한 데이터셋 MOSEI를 구축하기 위한 코드

## 📁 수집 과정에서 발생한 문제 📁

▶ 기존 문제 해결 접근법 : 

# 1. 사람 얼굴이 없는 동영상 => RetinaFace face detect
# 2. Frame freeze 영상 => Frame freeze detect
# 3. 비디오 리더기 에러 및 손상된 파일 =>  detect


▶ 현재 해결 접근법: 
▶ 기존에 갖고 있었던 어려움 : 선 수집후 동영상을 원하는 시간으로 자르면 다운로드의 시간이 30일 정도 걸림
▶ point : 처음부터 감정을 나타내는 시간 포인트에 해당되는 부분만 다운로드 할 수 있게 하자

#1. Frame freeze 영상 / 비디오 리더기 에러 및 손상된 파일
(1) ID 검출
(2) 세그먼트 별이 아닌 전체 영상 다운로드 후 파싱

#2. 사람 얼굴이 없는 동영상 
(1) Face Detecter Model인 RETINAFACE를 사용 [https://github.com/nanhungrybin/](https://github.com/nanhungrybin/Retinaface_torch)
(1) 전체 프레임 중 얼굴이 등장하지 않는 비율 검출
(2) 얼굴이 등장하지 않는 프레임 범위 검출 ▶ 추후 해당 프레임 제거한 후 dataset으로 사용 가능 / No Face 기준 논의 가능


## 📁 WHAT IS MOSEI 📁
![image](https://github.com/nanhungrybin/MOSEI_crawling/assets/97181397/c68f72c2-7292-46d0-b056-6bef5089eee7)

## 📁 WHY MOSEI 📁 왜 MOSEI는 중요한가? 왜 직접 수집해야하는가 ?

- 근로자 안전행동 수준의 영향요인을 검증하고 이를 기반으로 안전문화 평가 모형을 구축한다. (근로자 안전행동 수준을 기업의 안전문화 수준으로 확장해석하여 진행)

