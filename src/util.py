import urllib.request

class ImageSave:

    IMAGE_SAVE_PATH = "../img/"

    @staticmethod
    def url_save_image(filename: str, url: str) -> int:
        """ 이미지 URL을 받아서 저장하기 """
        try:
            save_path = ImageSave.IMAGE_SAVE_PATH + filename
            urllib.request.urlretrieve(url, save_path)
            return 0
        except:
            return -1

