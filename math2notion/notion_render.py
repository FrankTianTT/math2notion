import re
from typing import Union, Optional, List
from itertools import chain

from mistletoe import span_token, block_token
from mistletoe.token import Token
from mistletoe.span_token import SpanToken
from mistletoe.base_renderer import BaseRenderer
from notion_client import Client


class InlineEquation(SpanToken):
    parse_inner = False
    parse_group = 1
    pattern = re.compile(r"(?<!$)\$([^\n$]+?)\$(?!$)")


class Equation(SpanToken):
    parse_inner = False
    parse_group = 1
    pattern = re.compile(r'\$\$([^$]+?)\$\$')


class NotionRender(BaseRenderer):
    def __init__(self):
        super().__init__(InlineEquation, Equation)

    def render_inner(self, token) -> dict:
        return {
            'type': 'text',
            'text': {
                'content': token.content
            }
        }

    def get_rich_text_dict(
            self,
            content: str,
            text_type: str = "text",
            bold: bool = False,
            italic: bool = False,
            strikethrough: bool = False,
            underline: bool = False,
            code: bool = False,
            color: str = "default",
            href: Optional[str] = None
    ) -> dict:
        rich_text = {
            'type': text_type,
            text_type: {
                'content': content
            },
            "annotations": {
                "bold": bold,
                "italic": italic,
                "strikethrough": strikethrough,
                "underline": underline,
                "code": code,
                "color": color
            },
        }
        if href:
            rich_text[text_type]["link"] = {"url": href}
        return rich_text

    def render_raw_text(self, token) -> dict:
        return self.get_rich_text_dict(token.content)

    def render_strong(self, token: span_token.Strong) -> dict:
        assert hasattr(token, "children")
        assert len(token.children) == 1
        return self.get_rich_text_dict(token.children[0].content, bold=True)

    def render_emphasis(self, token: span_token.Emphasis) -> dict:
        return self.get_rich_text_dict(token.content, italic=True)

    def render_inline_code(self, token: span_token.InlineCode) -> dict:
        return self.get_rich_text_dict(token.content, code=True)

    def render_strikethrough(self, token: span_token.Strikethrough) -> dict:
        return self.get_rich_text_dict(token.content, code=True)

    def render_image(self, token: span_token.Image) -> dict:
        return {
            "type": "image",
            "image": {
                "type": "external",
                "external": {
                    "url": token.src
                }
            }
        }

    def render_link(self, token: span_token.Link) -> dict:
        return self.get_rich_text_dict(token.title, href=token.target)

    def render_auto_link(self, token: span_token.AutoLink) -> dict:
        return self.get_rich_text_dict(token.target, href=token.target)

    def render_escape_sequence(self, token: span_token.EscapeSequence) -> dict:
        return self.get_rich_text_dict(token.children[0].content)

    def render_line_break(self, token: span_token.LineBreak) -> dict:
        return self.get_rich_text_dict(" ")

    def get_container_dict(self, children: List[Token], container_type: str = "paragraph"):
        return {
            'type': container_type,
            container_type: {
                'rich_text': [self.render(child) for child in children]
            }
        }

    def render_heading(self, token: block_token.Heading) -> dict:
        level = token.level if token.level <= 3 else 3
        return self.get_container_dict(token.children, "heading_{}".format(level))

    def render_quote(self, token: block_token.Quote) -> dict:
        return self.get_container_dict(token.children, "quote")

    def render_paragraph(self, token: block_token.Paragraph) -> dict:
        return self.get_container_dict(token.children)

    def render_block_code(self, token: block_token.BlockCode) -> dict:
        return {
            "type": "code",
            "code": {
                "caption": [],
                "rich_text": [self.render(child) for child in token.children],
                "language": token.language
            }
        }

    def render_list(self, token: block_token.List) -> List[dict]:
        return [self.render(child) for child in token.children]

    def render_list_item(self, token: block_token.ListItem) -> dict:
        container_type = "bulleted_list_item" if token.leader == "-" else "numbered_list_item"
        return self.get_container_dict(token.children[0].children, container_type=container_type)

    def render_table(self, token: block_token.Table) -> dict:
        # TODO table
        raise NotImplementedError

    def render_table_cell(self, token: block_token.TableCell) -> dict:
        # TODO table
        raise NotImplementedError

    def render_table_row(self, token: block_token.TableRow) -> dict:
        # TODO table
        raise NotImplementedError

    def render_thematic_break(self, token: block_token.ThematicBreak) -> dict:
        return {
            "type": "divider",
            "divider": {}
        }

    def render_inline_equation(self, token: InlineEquation) -> dict:
        return {
            'type': 'equation',
            'equation': {
                'expression': token.content
            }
        }

    def render_equation(self, token: Equation) -> dict:
        return {
            'type': 'equation',
            'equation': {
                'expression': token.content
            },
        }

    def render_document(self, token: block_token.Document) -> list:
        blocks = []
        for child in token.children:
            if isinstance(child, block_token.List):
                blocks.extend(self.render(child))
            else:
                blocks.append(self.render(child))
        return blocks

    def upload(
            self,
            token: block_token.Document,
            notion_token: str,
            page_id: str,
            separately: bool = False
    ):

        notion = Client(auth=notion_token)
        if separately:
            for child in token.children:
                block = self.render(child)
                notion.blocks.children.append(
                    page_id,
                    children=block if isinstance(child, block_token.List) else [block]
                )
        else:
            notion.blocks.children.append(page_id, children=self.render(token))
