# 영수증 분석기 (Streamlit App)

이 프로젝트는 Google Vertex AI의 Gemini 모델을 사용하여 영수증 이미지를 분석하고, 상점 이름, 날짜, 총 금액, 품목 정보를 추출하는 Streamlit 애플리케이션입니다.

## 기능

* 지정된 폴더 내의 모든 영수증 이미지(.png, .jpg, .jpeg)를 자동으로 분석합니다.
* 각 영수증에 대한 분석 결과를 JSON 형태로 출력합니다.  JSON에는 다음 정보가 포함됩니다:
    * `store_name`: 상점 이름
    * `date_time`: 날짜 및 시간
    * `total_cost`: 총 금액
    * `items`: 품목 목록 (각 품목은 `item_name`, `quantity`, `unit_price`, `amount` 정보를 포함)
* 분석 결과와 함께 원본 영수증 이미지를 Streamlit UI에 표시합니다.
* Google Cloud Platform (GCP)의 Vertex AI와 Gemini 모델을 활용합니다.


## 사용 방법

1. **필수 사항:**
    * Python 3.7 이상 설치
    * Google Cloud Platform 프로젝트 및 Vertex AI API 활성화
    * `google-cloud-aiplatform`, `streamlit`, `Pillow`, `python-dotenv`, `vertexai`, `mimetypes`, `re` 패키지 설치:
      ```bash
      pip install google-cloud-aiplatform streamlit Pillow python-dotenv vertexai mimetypes re
      ```
2. **환경 설정:**
    * `.env` 파일을 생성하고 다음 변수를 설정합니다.  `PROJECT`는 GCP 프로젝트 ID, `LOCATION`은 Vertex AI 모델 위치 (예: `us-central1`)입니다.
      ```
      PROJECT="YOUR_PROJECT_ID"
      LOCATION="us-central1"
      ```
3. **영수증 이미지 준비:**
    * 분석할 영수증 이미지를 `.png`, `.jpg`, 또는 `.jpeg` 형식으로 폴더에 저장합니다.
4. **Streamlit 앱 실행:**
    ```bash
    streamlit run app.py
    ```
5. **폴더 경로 입력:**
    * Streamlit 앱의 왼쪽 사이드바에 영수증 이미지가 있는 폴더의 경로를 입력합니다.
6. **분석 실행:**
    * "분석" 버튼을 클릭합니다.
7. **결과 확인:**
    * 앱은 각 영수증 이미지와 해당 분석 결과 JSON을 표시합니다.


## 폴더 구조

```
영수증 분석기/
├── app.py       (메인 스트림릿 애플리케이션 파일)
└── .env         (GCP 프로젝트 ID와 위치를 포함하는 환경 설정 파일)
```

## 제한 사항

* 이미지 품질, 영수증 형식, 언어 등에 따라 분석 정확도가 달라질 수 있습니다.
* Gemini 모델의 사용량에 따라 비용이 발생할 수 있습니다.  GCP 콘솔에서 사용량을 모니터링하세요.
*  `.env` 파일을 Git 저장소에 추가하지 마세요.  `PROJECT`와 `LOCATION` 변수를 안전하게 관리하는 방법을 고려하세요 (예: GCP Secret Manager).


## 추가 기능 (미래 개발)

* 사용자 인터페이스 개선
* 다양한 이미지 형식 지원
* 오류 처리 및 사용자 피드백 향상
* 분석 결과 다운로드 기능 추가


이 README 파일은 프로젝트의 개요와 사용 방법을 설명합니다.  더 자세한 내용은 소스 코드를 참조하십시오.