from notion_connect import NotionConnect
from notion import block


class BlockToMarkdown:
    """
        노션에서 얻은 block type을 마크다운 형태로 변경합니다.

        모든 블럭이 지원되지는 않습니다.
        - Date : 2022-01-22

    """

    def __init__(self, block_list: list) -> None:
        self.block_list: list = block_list
        self.markdown_list: list = []
        self._change_blocks()
        self._show_block_list()
        self._show_markdown_list()

    def _show_markdown_list(self) -> None:
        """markdown_list 보여주기"""
        for row in self.markdown_list:
            print(row)

    def _show_block_list(self) -> None:
        """block_list 보여주기"""
        print(self.block_list)

    def _change_blocks(self):
        """page의 모든 notion 블럭 마크다운으로 변경"""
        for index, block_row in enumerate(self.block_list):

            # 빈 block
            if isinstance(block_row, block.TextBlock) and block_row.title == "":
                self.markdown_list.append(
                    (index, self._empty_block(block_row))
                )

            # text block ( 글 )
            elif isinstance(block_row, block.TextBlock):
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
                    (index, self._bullete_list_block(block_row))
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
    def _bullete_list_block(cls, block: block.BulletedListBlock, tab_count: int=0) -> str:
        """bullete_list 블럭 마크 다운 형태로 변경"""
        tab = tab_count * '\t'
        markdown = f"- {tab}{block.title}\n"
        for children_block in block.children:
            markdown += cls._bullete_list_block(children_block, tab_count + 1)

        return markdown


if __name__ == '__main__':
    # --------------------- 블럭 얻기 --------------------- #
    PAGE_URL = "https://www.notion.so/d2094f33336f4139af28bd5ba51af92b"
    NC1 = NotionConnect()
    NC1.connect_token_v2_key()
    block_list = NC1.get_block(PAGE_URL)
    # ---------------------------------------------------- #
    BM = BlockToMarkdown(block_list.children)





