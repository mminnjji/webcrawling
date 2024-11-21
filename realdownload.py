from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# ChromeDriver 경로 설정
CHROMEDRIVER_PATH = 'C:/chromedriver-win64/chromedriver.exe'
TARGET_URL = "https://9xbuddy.in/ko"
INPUT_FILE = "security.txt"  # URL 리스트가 담긴 텍스트 파일
OUTPUT_FILE = "security_download_links.txt"

# Selenium WebDriver 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 필요 시 headless 모드
options.add_argument('--disable-cache')  # 캐시 비활성화
driver_service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=driver_service, options=options)

def clear_cookies_and_refresh():
    """브라우저 쿠키를 삭제하고 페이지 새로 고침"""
    driver.delete_all_cookies()
    print("쿠키 삭제 완료. 페이지 새로고침.")
    driver.refresh()
    time.sleep(3)  # 새로고침 후 대기

def extract_download_link():
    """'지금 다운로드하십시오' 버튼의 링크를 추출하여 기록"""
    try:
        span_elements = driver.find_elements(By.XPATH, "//span[text()='지금 다운로드하십시오']")
        with open(OUTPUT_FILE, 'a') as output_file:
            for span in span_elements:
                try:
                    parent_a_tag = span.find_element(By.XPATH, "./ancestor::a")
                    download_url = parent_a_tag.get_attribute("href")
                    output_file.write(f"{download_url}\n")
                    print(f"파일 다운로드 URL 기록됨: {download_url}")
                    return True  # 성공하면 함수 종료
                except Exception as e:
                    print(f"다운로드 URL 추출 오류: {e}")
        return False
    except NoSuchElementException:
        print("다운로드 버튼을 찾을 수 없습니다.")
        return False

def process_url(url):
    """주어진 URL을 처리"""
    try:
        # 대상 사이트로 이동
        driver.get(TARGET_URL)
        time.sleep(3)  # 페이지 로드 대기

        # 입력 필드에 URL 입력
        input_element = driver.find_element(By.CSS_SELECTOR, 'input[name="text"]')
        input_element.send_keys(url)

        # 다운로드 버튼 클릭
        download_button = driver.find_element(By.XPATH, "//button[text()='다운로드']")
        download_button.click()
        time.sleep(5)  # 리디렉션 대기

        # 다운로드 링크 추출
        success = extract_download_link()
        if not success:
            # 실패 시 쿠키 삭제 및 재시도
            clear_cookies_and_refresh()
            input_element = driver.find_element(By.CSS_SELECTOR, 'input[name="text"]')
            input_element.send_keys(url)
            download_button = driver.find_element(By.XPATH, "//button[text()='다운로드']")
            download_button.click()
            time.sleep(5)
            success = extract_download_link()
            if not success:
                print(f"URL 처리 실패: {url}")
    except Exception as e:
        print(f"URL 처리 중 오류 발생 ({url}): {e}")

try:
    # 텍스트 파일에서 URL 읽기
    with open(INPUT_FILE, 'r') as file:
        urls = file.readlines()

    for line in urls:
        url = line.strip()
        if url:
            print(f"처리 중: {url}")
            process_url(url)
except Exception as e:
    print(f"스크립트 오류: {e}")
finally:
    # 브라우저 종료
    driver.quit()
