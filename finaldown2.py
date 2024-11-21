import os
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

# Google Drive API 인증 정보
SERVICE_ACCOUNT_FILE = r'C:\Users\pureh\webcrawling\principal-yen-442316-v1-c536e1d66af6.json'  # 서비스 계정 JSON 파일 경로
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Google Drive API 클라이언트 생성
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

def download_video(video_url, save_path):
    """
    URL에서 MP4 파일 다운로드
    """
    try:
        print(f"비디오 다운로드 시작: {video_url}")
        response = requests.get(video_url, stream=True)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생

        # 파일 저장
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"비디오 다운로드 완료: {save_path}")
    except Exception as e:
        print(f"비디오 다운로드 실패: {e}")
        raise

def upload_to_google_drive(file_path, file_name, folder_id):
    """
    Google Drive의 특정 폴더에 파일 업로드
    """
    try:
        print(f"Google Drive로 업로드 시작: {file_path}")
        # 업로드 대상 폴더 지정
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]  # 업로드 대상 폴더 ID 지정
        }
        media = MediaFileUpload(file_path, mimetype='video/mp4')
        
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"파일 업로드 완료. 파일 ID: {uploaded_file.get('id')}")
        return uploaded_file.get('id')
    except Exception as e:
        print(f"Google Drive 업로드 실패: {e}")
        raise

def delete_local_file(file_path):
    """
    로컬 파일 삭제
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"로컬 파일 삭제 완료: {file_path}")
        else:
            print(f"파일이 존재하지 않습니다: {file_path}")
    except Exception as e:
        print(f"로컬 파일 삭제 실패: {e}")
        raise

# 메인 함수
if __name__ == '__main__':
    input_file = 'sw_download_links.txt'  # 다운로드 링크가 저장된 파일
    local_file_path = "downloaded_2video.mp4"  # 다운로드된 파일의 임시 경로
    folder_id = '1-qmujso8zb8CxXOD4PosEA1cz2b-c8Bx'  # Google Drive 업로드 대상 폴더 ID
    episode_number = 68  # 회차 번호 초기값

    try:
        # tmp.txt에서 한 줄씩 읽기
        with open(input_file, 'r') as file:
            for line in file:
                video_url = line.strip()
                if not video_url:
                    continue  # 빈 줄은 건너뜀

                try:
                    # 1. 비디오 다운로드
                    download_video(video_url, local_file_path)
                    
                    # 2. 업로드 파일명 생성
                    file_name = f"소공_{episode_number}.mp4"
                    
                    # 3. Google Drive로 업로드
                    upload_to_google_drive(local_file_path, file_name, folder_id)
                    
                    # 4. 로컬 파일 삭제
                    delete_local_file(local_file_path)

                    # 회차 번호 증가
                    episode_number += 1

                except Exception as process_error:
                    print(f"URL 처리 중 오류 발생: {video_url}, 오류: {process_error}")
    except Exception as e:
        print(f"파일 처리 중 오류 발생: {e}")
