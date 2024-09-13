from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# WebDriver 경로 설정 (ChromeDriver)
chrome_service = Service('C:/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=chrome_service)

# 입력 파일 경로 및 URL
input_file_path = './sogong.txt'
url = 'https://9xbuddy.in/ko'
output_file_path = './download_urls.txt'

# 파일의 각 줄을 읽어서 처리
with open(input_file_path, 'r') as file:
    lines = [line.strip() for line in file.readlines()]

# 결과를 기록할 파일 열기
with open(output_file_path, 'w') as output_file:
    # 각 라인에 대해 작업 수행
    for line in lines:
        # 웹사이트 열기 및 페이지 로드 대기
        driver.get(url)
        time.sleep(3)
        
        try:
            # 입력 필드에 텍스트 입력
            input_element = driver.find_element(By.CSS_SELECTOR, 'input[name="text"]')
            input_element.send_keys(line)
            
            # 다운로드 버튼 클릭
            download_button = driver.find_element(By.XPATH, "//button[text()='다운로드']")
            download_button.click()

            # 페이지 리다이렉션 대기
            time.sleep(10)

            # '지금 다운로드하십시오' 텍스트가 포함된 <span> 태그 찾기
            span_elements = driver.find_elements(By.XPATH, "//span[text()='지금 다운로드하십시오']")

            # 여러 버튼이 있을 수 있으므로 반복 처리
            for span in span_elements:
                try:
                    # span 태그의 직계 부모인 a 태그 찾기
                    parent_a_tag = span.find_element(By.XPATH, "./ancestor::a")
                    
                    # href 속성 추출 및 다운로드 URL 기록
                    download_url = parent_a_tag.get_attribute("href")
                    output_file.write(f"{download_url}\n")
                    
                    # 접속 성공 시 break
                    print(f"파일 다운로드 URL 기록됨: {download_url}")
                    break
                except Exception as e:
                    print(f"다운로드 URL 추출 오류: {e}")
        
        except Exception as e:
            print(f"페이지 처리 오류: {e}")

# 브라우저 닫기
driver.quit()
