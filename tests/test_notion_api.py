from notion_client import Client

from tests import notion_token, page_id


def test_api():
    notion = Client(auth=notion_token)
    equation = {
        'type': 'equation',
        'equation': {
            'expression': r'\frac{1}{2}'
        }
    }

    notion.blocks.children.append(page_id, children=[equation])
