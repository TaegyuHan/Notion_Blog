import unittest
from src.google_drive_connect import GoogleDriveConnect

class TestBlockToMarkdown(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """테스트를 실행할 때 단 1번 실행 됩니다."""
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        """테스트를 끝낼 때 단 1번 실행 됩니다."""
        print('teardownClass')

    def setUp(self):
        """각각의 테스트 메소드가 실행될 때 실행 됩니다."""
        print('setUp')

    def tearDown(self):
        """각각의 테스트 메소드가 끝날 때 실행 됩니다."""
        print('tearDown\n')

    def test_make_folder(self):
        """ google API 폴더 생성 """
        GoogleDriveConnect.make_folder(
            folder_id=GoogleDriveConnect.BLOG_IMAGE_FOLDER_ID,
            folder_name="new_folder2"
        )

