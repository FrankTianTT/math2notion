import argparse

import pypandoc
from mistletoe import Document

from math2notion.notion_render import NotionRender

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Math2Notion: Convert from LaTeX or Markdown to Notion')

    parser.add_argument('-s', '--source', type=str, required=True)
    parser.add_argument('-t', '--notion_token', type=str, required=True)
    parser.add_argument('-i', '--page_id', type=str, required=True)

    args = parser.parse_args()

    render = NotionRender()
    with open(args.source) as f:
        if args.source.endswith(".tex"):
            md_text = pypandoc.convert_text(f.read(), "md", "tex")
        else:
            md_text = f.read()
        doc = Document(md_text)
        render.upload(doc, args.notion_token, args.page_id)
