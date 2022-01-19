# Inssajeon-newly-coined-word 📖

you can use this service through [chromeExtension](https://github.com/spqjf12345/Inssajeon-newly-coined-word/tree/main/ChromeExtension) 🔝


---


# 인싸전 - 당신을 위한 신조어 사전 📖

**인싸전**은 **'인싸 + 사전'** 의 합성어로 한글 신조어 사전입니다.

**1️⃣ 개발 동기** 

인터넷 사용 중 모르는 신조어가 등장할 때 주변 사람에게 물어보거나 포털 사이트에 검색을 해보는 번거로운 경험이 한번쯤 있으셨나요 ?
신조어는 생성 및 소멸 속도가 매우 빠르고 그 폭이 넓어 의미 파악이 어렵습니다. 
따라서 급변하는 신조어에 대응하여 세대간 장벽 없는 소통을 위해 웹페이지에서 툴팁 형태로 신조어의 의미를 파악할 수 있게끔 편리한 서비스를 개발하고자 하였습니다.

---

**2️⃣ 의미 분석 주요 기능** 

  - 문장 크롤링
  
다양한 연령대가 사용하는 신조어를 고루 추출하기 위해 클리앙, 디시인사이드의 제목과 유튜브 인기동영상의 댓글을 크롤링
  
  - 데이터 전처리

파이썬의 beautiful soup 패키지와 정규 표현식을 이용해 알파벳 특수문자, ‘ㅋ'남발, 정치, 종교, 욕설 등의 금칙어 제거의 전처리 과정을 거친 뒤 정제
  
  - 신조어 추출 
 
한국어 형태소 분석기 Soynlp를 이용하여 모든 문장을 학습시킨 뒤 또 다른 형태소 분석기인 Konlpy의 okt noun을 교집합하여 문장을 토크나이징

단어가 표준성을 띄는지 검사하기 위해 맞춤법 검사기 hunspell과 sejong corpus를 거쳐 필터링 한 뒤 신조어 후보 단어로 채택
  
  - 카테고리 분석
  
1D- CNN 을 활용해 **초성어, 합성어, 줄임말, 기타**로 단어를 카테고리화 

Komoran 형태소 분석기를 활용해 단어의 pos tagging 값을 도출한 뒤 TF-IDF로 벡터화 시킨 단어 벡터들을 1D- CNN 모델에 주입
  
  - 유사 단어 분석

word2vec보다 더 정밀한 단위로 유사도를 검사하여 Fasttext를 활용해 주변 단어 분석

이를 wordcloud로 시각화하여 상위 10개 단어 제공
  
  - 감성 분석
 
word2vec보다 더 정밀한 단위로 유사도를 검사하여 Fasttext를 활용해 주변 단어 분석

이를 wordcloud로 시각화하여 상위 10개 단어 제공


---

  
**3️⃣  기술 스택**

  - 주언어 : Python 
  
  - 신조어 추출 : Python selenium, beautiful soup 
  
  - 형태소 분석 : Konlpy - okt, komoran / Soynlp - MaxScoreTokenizer
  
  - 모델 생성 : tensorflow 프레임워크
  
  - 웹서버 : AWS EC2, Flask 
  
  - 감성 사전 : KNU 감성 사전 
  
  - 확장 프로그램 : html, css, javaScript 
  

---


**3️⃣ 예시 화면** 

<p align="center">
    <img width="387" alt="스크린샷 2021-02-25 오후 7 19 14" src="https://user-images.githubusercontent.com/50979257/109139065-6b14de80-779e-11eb-9ebe-5e3091efe718.png" width="700" height="370">
  </p>
  
  
--- 
  
  
  
  
  
  
  
  
(위 프로젝트는 별도의 추가적 파일이 필요합니다. 
사용이 필요하신 분들은 📧 spqjf12345@gmail.com으로 편하게 연락주세요 🙋🏻‍♀️)


  

