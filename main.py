import streamlit as st
import os
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import json
from PIL import Image
import io
from dotenv import load_dotenv
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import mimetypes
import re

# .env 파일 로드
load_dotenv()

PROJECT=os.getenv("PROJECT")
LOCATION=os.getenv("LOCATION")


# Vertex AI 초기화
vertexai.init(project=PROJECT, location=LOCATION)
model = GenerativeModel(
    "gemini-1.5-flash-002",
)

def get_image_data(image_path):
    with open(image_path, 'rb') as image_file:
        return image_file.read()

def get_mime_type(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    return mime_type or 'application/octet-stream'

def fix_json_quotes(json_string):
    return re.sub(r"(?<!\\)'", '"', json_string)

def extract_json_value(json_str):
    start_index = json_str.find('```json') + 7
    end_index = json_str.find('```', start_index)
    json_str = json_str[start_index:end_index].strip()
    cleaned_string = json_str.replace('\\xa0', ' ')
    print(cleaned_string)
    try:
        return_json = json.loads(cleaned_string)
    except:
        return_json = json.loads(fix_json_quotes(cleaned_string))
    return return_json

def analyze_receipt(image_path):
    text1 = """주어진 영수증 이미지에 대하여, 다음 정보를 추출해서 JSON으로 출력해 주세요. 

output : 
{ \"store_name\" : \"...\",
  \"date_time\" : \"...\",
  \"total_cost\" : ... ,
  \"items\" : [ { \"item_name\" : \"...\" , \"quantity\" : ... , \"unit_price\": ... , \"amount\" : ... } ]
}

Image :"""

    image1 = Part.from_data(get_image_data(image_path), mime_type=get_mime_type(image_path))
    generation_config = {
      "max_output_tokens": 8192,
      "temperature": 1,
      "top_p": 0.95,
    }
    safety_settings = [
      SafetySetting(
          category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
          threshold=SafetySetting.HarmBlockThreshold.OFF
      ),
      SafetySetting(
          category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
          threshold=SafetySetting.HarmBlockThreshold.OFF
      ),
      SafetySetting(
          category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
          threshold=SafetySetting.HarmBlockThreshold.OFF
      ),
      SafetySetting(
          category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
          threshold=SafetySetting.HarmBlockThreshold.OFF
      ),
    ]

    responses = model.generate_content(
        [text1, image1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )

    # 응답에서 JSON 추출
    response_json = extract_json_value(responses.candidates[0].content.text)
    
    return response_json

def main():
    st.title("영수증 분석기")
    
    # 왼쪽 사이드바에 폴더 선택 위젯 추가
    folder_path = st.sidebar.text_input("영수증 이미지가 있는 폴더 경로를 입력하세요:")
    
    if folder_path and os.path.isdir(folder_path):
        # 분석 버튼
        if st.sidebar.button("분석"):
            # 폴더 내 이미지 파일 목록 가져오기
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # 각 이미지에 대해 분석 수행
            for image_file in image_files:
                image_path = os.path.join(folder_path, image_file)
                
                # 이미지 분석
                json_result = analyze_receipt(image_path)
                
                # 결과 표시
                col1, col2 = st.columns(2)
                
                with col1:
                    st.image(Image.open(image_path), caption=image_file, use_column_width=True)
                
                with col2:
                    st.json(json_result)
                
                st.markdown("---")  # 구분선 추가
    else:
        st.sidebar.warning("올바른 폴더 경로를 입력해주세요.")

if __name__ == "__main__":
    main()