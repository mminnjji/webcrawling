from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

# Chrome 드라이버 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않고 실행
chrome_driver_path = 'C:/chromedriver-win64/chromedriver.exe'  # 드라이버 경로에 맞게 수정

# 크롬 드라이버 시작
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

# 로그인 페이지 접근
login_url = 'https://pass25.com/wp-login.php'
driver.get(login_url)
time.sleep(2)  # 페이지 로드 대기

# 로그인 과정 수행
try:
    # ID와 비밀번호 입력
    email_input = driver.find_element(By.ID, 'user_login')  # ID 필드 찾기 (정확한 ID로 변경)
    password_input = driver.find_element(By.ID, 'user_pass')  # 비밀번호 필드 찾기 (정확한 ID로 변경)

    email_input.send_keys('9336pure')  # 본인의 이메일 입력
    password_input.send_keys('Mminji010115!')  # 본인의 비밀번호 입력

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.ID, 'wp-submit')  # 로그인 버튼의 ID (정확한 ID로 변경)
    login_button.click()

    time.sleep(3)  # 로그인 처리 대기

except Exception as e:
    print(f"로그인 실패: {e}")
    driver.quit()
    exit()

# 로그인 후 원하는 페이지로 이동
start_url = 'https://pass25.com/course/%ec%86%8c%ed%94%84%ed%8a%b8%ec%9b%a8%ec%96%b4%ea%b3%b5%ed%95%99-%ea%b8%b0%eb%b3%b8-%ec%9d%b4%eb%a1%a0/%ec%86%8c%ea%b3%b5_%ec%a3%bc%ec%a0%9c_%ea%b5%ad%ec%a0%9c%ed%91%9c%ec%a4%80-2/'
driver.get(start_url)
time.sleep(3)

# 동영상 링크를 저장할 파일
output_file = 'output.txt'

# 페이지 HTML 저장
def extract_video_link():
    try:
        # iframe이 로드될 때까지 기다립니다. 
        # iframe이 여러 개 있는 경우 특정 속성으로 iframe을 찾도록 수정.
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='dubb.com']"))
        )
        
        # iframe에서 src 속성 추출
        video_url = iframe.get_attribute('src')
        print(f"동영상 링크: {video_url}")

        # 파일에 동영상 링크 기록
        with open(output_file, 'a') as f:
            f.write(video_url + '\n')

    except Exception as e:
        print(f"동영상 링크 추출 실패: {e}")

def go_to_next_lecture():
    try:
        # 현재 active 상태의 강의(li)를 찾음
        current_lecture = driver.find_element(By.CSS_SELECTOR, "li.unit_line.active")
        
        # 현재 강의의 다음 li 요소를 찾음
        next_lecture = current_lecture.find_element(By.XPATH, './following-sibling::li[1]/a')

        # 다음 강의 클릭
        next_lecture.click()
        time.sleep(2)  # 페이지 로드 대기
        return True  # 다음 강의로 이동 성공

    except Exception as e:
        print(f"다음 강의로 이동 실패: {e}")
        return False  # 다음 강의로 이동 실패


# 메인 루프
while True:
    # 동영상 링크 추출
    extract_video_link()

    # 다음 강의로 이동, 없으면 종료
    if not go_to_next_lecture():
        break

# 크롬 드라이버 종료
driver.quit()

print(f"동영상 링크가 {output_file} 파일에 저장되었습니다.")