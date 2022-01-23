from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
class GoogleDriveConnect:
    """ 구글 드라이브 연동 """

    SCOPES = ['https://www.googleapis.com/auth/drive']
    CREDENTIALS_PATH = "../json/credentials.json"
    TOKEN_PATH = '../json/token.json'
    BLOG_IMAGE_FOLDER_ID = "1k-5yMzjEUCupxzRooGDxvplRmjSnRLDW"

    # 구글 드라이브 연동 확인
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            TOKEN_PATH,
            SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    @classmethod
    def get_folder_or_file_list(cls, folder_id: str) -> dict[str:str]:
        """ 구글 드라이브 폴더 ID의 폴더, 파일 반환

        :param folder_id: 구글 드라이브 폴더 ID
        :return: 파일, 폴더 이름: 해당 ID
        """
        try:
            service = build('drive', 'v3', credentials=cls.creds)
            
            # 폴더 검색
            results = service.files().list(
                q=f"parents in '{folder_id}'", # Blog_Image folder Path
                fields="files(id, name), incompleteSearch, nextPageToken").execute()

            # 폴더 저장
            items = results['files']
            file_or_folders = {}

            # 현재 경로의 파일 또는 폴더 출력
            for folder_or_file in items:
                file_or_folders[folder_or_file['name']] = folder_or_file['id']

            return file_or_folders

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    @classmethod
    def make_folder(cls, folder_id: str, folder_name: str) -> tuple[str, str]:
        """ 폴더 아이디를 받아서 그 안에 폴더를 새로 생성합니다.

            기존에 폴더가 존재하면 그 폴더의 ID를 반환합니다.

        :param folder_id: 구글 드라이브 폴더 ID
        :param folder_name: 새로 생성할 폴더 이름
        :return: 새로 생성한 폴더 ID
        """

        # 이미 존재하는 폴더인지 확인
        exists_folders = cls.get_folder_or_file_list(folder_id)
        if folder_name in exists_folders.keys():
            # 있으면 그 폴더의 ID 반환
            return folder_name, exists_folders[folder_name]

        try:
            service = build('drive', 'v3', credentials=cls.creds)
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [folder_id]
            }
            # 폴더 생성
            file = service.files().create(body=file_metadata,
                                          fields='id').execute()

            return folder_name, file.get("id")

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')


    def __call__(cls, *args, **kwargs):
        """싱글톤 패턴"""
        if cls._instances is None:
            cls._instances = GoogleDriveConnect()
            return cls._instances
        return cls._instances


if __name__ == '__main__':
    g = GoogleDriveConnect()
    g2 = GoogleDriveConnect()
    root_folders = g.get_folder_or_file_list(GoogleDriveConnect.BLOG_IMAGE_FOLDER_ID)
    g.make_folder(folder_id=GoogleDriveConnect.BLOG_IMAGE_FOLDER_ID,
                  folder_name="new_folder2")


