import unittest
from src.util import ImageSave

class TestImageSave(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """테스트를 실행할 때 단 1번 실행 됩니다."""
        print('Run : setupClass')

    @classmethod
    def tearDownClass(cls):
        """테스트를 끝낼 때 단 1번 실행 됩니다."""
        print('Run : teardownClass')

    def setUp(self):
        """각각의 테스트 메소드가 실행될 때 실행 됩니다."""
        print('Run : setUp')

    def tearDown(self):
        """각각의 테스트 메소드가 끝날 때 실행 됩니다."""
        print('Run : tearDown\n')

    def test_url_save_image(self):
        """ URL 이미지 받아서 저장하기  """
        ImageSave.url_save_image(
            filename="url_img.jpg",
            url="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/b946b74a-718a-4a9f-9a24-995f07267db8/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220123%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220123T141141Z&X-Amz-Expires=86400&X-Amz-Signature=0cfef89eada328b568841d984955135b6836e1d83737f2d2322db1b5ea5dbb7f&X-Amz-SignedHeaders=host&x-id=GetObject"
        )