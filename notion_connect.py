import json
from notion.client import NotionClient

# --------------------------------------------------------------- #
# notion 라이브러리 에러!
# URL https://github.com/jamalex/notion-py/pull/352/commits/fe8ac41e1c10a229c040bd7cadd9429a66fbcda3
# 에러 해결 링크 : queryCollection 요청 페이로드 및 응답 구문 분석 변경
# --------------------------------------------------------------- #

class NotionConnect:
    """
        노션 라이블러리 연결
    """
    NOTION_KEY_FILE: str = f"./json/notion.json"
    NOTION_KEY: dict = None
    CLIENT: NotionClient = None

    _instance = None # 싱글턴 확인

    @classmethod
    def connect_token_v2_key(cls) -> None:
        """노션 token_v2 불러오기"""
        with open(cls.NOTION_KEY_FILE, 'r') as f:
            cls.NOTION_KEY = json.load(f)

        if cls.CLIENT is None:
            cls.CLIENT = NotionClient(token_v2=cls.NOTION_KEY["token_v2"])

    def __call__(cls, *args, **kwargs):
        """싱글톤 패턴"""
        if cls._instances is None:
            cls._instances = NotionConnect()
            return cls._instances
        return cls._instances

    @classmethod
    def get_block(cls, collection_page_url: str) -> list:
        """ 노션 copy URL을 입력받아서 입력 받은 URL의
            블럭을 반환 합니다.

        :param URL: 노션의 copy URL
        :return: 입력받은 URL의 블럭을 반환합니다.
        """

        collection_block = cls.CLIENT.get_block(collection_page_url)
        return collection_block

    # @staticmethod
    # def get_children(block_id: str) -> None:
    #     # print(block_id)
    #     client = NotionClient(token_v2=cls.NOTION_KEY["token_v2"])
    #     block = client.get_block(collection_page_url)
    #     pass

if __name__ == '__main__':
    # PAGE_URL = "https://www.notion.so/d2094f33336f4139af28bd5ba51af92b"
    # NC1 = NotionConnect()
    # NC1.connect_token_v2_key()
    # # print(NC1.get_block(PAGE_URL))
    # black = NC1.get_block("e7c23bdc-f4d9-4ef2-af06-1485ad67637a")
    # print(black.children)
    pass