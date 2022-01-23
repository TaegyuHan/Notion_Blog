import urllib.request
from notion_connect import NotionConnect
from google_drive_connect import GoogleDriveConnect
from notion import block


class BlockToMarkdown:
    """
        노션에서 얻은 block type을 마크다운 형태로 변경합니다.

        모든 블럭이 지원되지는 않습니다.
        - Date : 2022-01-22
    """

    def __init__(self, block_list: list, block_properties: dict) -> None:
        self.block_list: list = block_list
        self.markdown_list: list = []
        self._show_block_list()
        self._show_markdown_list()
        self.numbered_list_number: int = 1

        # 새로 생성할 이미지 저장 폴더
        self.category_folder = block_properties["category"]
        self.page_name_folder = \
            f'{block_properties["date"].start}-{block_properties["file_name"]}'

        # notion블럭 markdown 형태로 변경
        self._change_blocks()

    def _show_markdown_list(self) -> None:
        """markdown_list 보여주기"""
        for row in self.markdown_list:
            print(row)

    def _show_block_list(self) -> None:
        """block_list 보여주기"""
        print(self.block_list)

    def _change_blocks(self) -> None:
        """page의 모든 notion 블럭 마크다운으로 변경"""
        for index, block_row in enumerate(self.block_list):

            # 빈 block
            if isinstance(block_row, block.TextBlock) and block_row.title == "":
                self.markdown_list.append(
                    (index, self._empty_block(block_row))
                )

            # text block ( 글 )
            elif isinstance(block_row, block.TextBlock):

                try: # 이전의 block이 image이면 pass
                    if isinstance(self.block_list[index - 1], block.ImageBlock):
                        continue
                except IndexError as e:
                    pass # 맨처음 text block

                self.markdown_list.append(
                    (index, self._text_block(block_row))
                )

            # div block ( 나눔선 )
            elif isinstance(block_row, block.DividerBlock):
                self.markdown_list.append(
                    (index, self._div_block(block_row))
                )

            # codeBox block ( 코드박스 )
            elif isinstance(block_row, block.CodeBlock):
                self.markdown_list.append(
                    (index, self._code_box_block(block_row))
                )

            # Bulleted List block ( 일반 리스트 )
            elif isinstance(block_row, block.BulletedListBlock):
                self.markdown_list.append(
                    (index, self._bulleted_list_block(block_row))
                )

            # Numbered List block ( 숫자 리스트 )
            elif isinstance(block_row, block.NumberedListBlock):

                # 전에도 Numbered List 인지 확인
                if isinstance(self.block_list[index - 1], block.NumberedListBlock):
                    self.numbered_list_number += 1
                # 전에 Numbered List 가 없으면 1로 초기화
                else:
                    self.numbered_list_number = 1

                self.markdown_list.append(
                    (index, self._numbered_list_block(
                        block=block_row,
                        frist_number=self.numbered_list_number))
                )

            # Image block ( 이미지 )
            elif isinstance(block_row, block.ImageBlock):
                next_block = self.block_list[index + 1]

                # image block 다음의 text블럭
                if isinstance(next_block, block.TextBlock):
                    image_text = self._text_block(next_block)

                notion_image_url = block_row.source

                # 구글 드라이브 연동
                GDC = GoogleDriveConnect()

                # 카테고리 폴더 생성
                category_folder_id = GDC.make_folder(
                    folder_id=GDC.BLOG_IMAGE_FOLDER_ID,
                    folder_name=self.category_folder
                )

                # 페이지 폴더 생성
                page_name_folder_id = GDC.make_folder(
                    folder_id=category_folder_id,
                    folder_name=self.page_name_folder
                )

                # token횟수 제안!! 확인 필요
                self.markdown_list.append(
                    (index, self._image_block(block_row))
                )

    @staticmethod
    def _empty_block(block: block.TextBlock) -> str:
        """빈 블럭 마크 다운 형태로 변경"""
        return "<br>\n"

    @staticmethod
    def _text_block(block: block.TextBlock) -> str:
        """text 블럭 마크 다운 형태로 변경"""
        return f"{block.title}\n"

    @staticmethod
    def _div_block(block: block.DividerBlock) -> str:
        """div 블럭 마크 다운 형태로 변경"""
        return f"---\n"

    @staticmethod
    def _code_box_block(block: block.CodeBlock) -> str:
        """code box 블럭 마크 다운 형태로 변경"""
        return f"```\n{block.title}```"

    @classmethod
    def _bulleted_list_block(cls, block: block.BulletedListBlock, tab_count: int=0) -> str:
        """bullete_list 블럭 마크 다운 형태로 변경"""
        tab = tab_count * '\t'
        markdown = f"{tab}- {block.title}\n"
        for children_block in block.children:
            markdown += cls._bulleted_list_block(children_block, tab_count + 1)

        return markdown

    @classmethod
    def _numbered_list_block(cls,
                             block: block.BulletedListBlock,
                             tab_count: int=0,
                             frist_number: int=1) -> str:
        """numbered_list 블럭 마크 다운 형태로 변경

        :param block: notion 블럭
        :param tab_count: 탭 횟수
        :param frist_number: 숫자 리스트 첫번째 번호 입력
        :return: 마크다운 형식으로 변경
        """
        tab = tab_count * '\t'
        markdown = f"{tab}{frist_number}. {block.title}\n"
        for i, children_block in enumerate(block.children):
            markdown += cls._numbered_list_block(
                block=children_block,
                tab_count=tab_count + 1,
                frist_number=i + 1)

        return markdown

    @classmethod
    def _image_block(cls, block: block.ImageBlock) -> str:
        """이미지 블럭 마크 다운 형태로 변경"""
        # 구글 드라이브랑 연동해야함



if __name__ == '__main__':
    # --------------------- 블럭 얻기 --------------------- #
    PAGE_URL = "https://www.notion.so/d2094f33336f4139af28bd5ba51af92b"
    NC1 = NotionConnect()
    NC1.connect_token_v2_key()
    block_list = NC1.get_block(PAGE_URL)
    block_properties = block_list.get_all_properties()

    # ---------------------------------------------------- #
    BM = BlockToMarkdown(
        block_list=block_list.children,
        block_properties=block_properties)