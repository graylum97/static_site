from enum import Enum

from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    split_markdown = markdown.split("\n\n")

    for block in split_markdown:
        block = block.strip(" \n")
        if block != "":
            blocks.append(block)
    return blocks

def block_to_block_type(block):
    if (
        block.startswith("# ") or block.startswith("## ") or
        block.startswith("### ") or block.startswith("#### ") or
        block.startswith("##### ") or block.startswith("###### ")
    ):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith('>'):
        lines = block.split('\n')
        is_quote = True

        for line in lines:
            if not line.startswith('>'):
                is_quote = False
                break

        if is_quote:
            return BlockType.QUOTE

    if block.startswith("- "):
        lines = block.split('\n')
        is_unordered_list = True

        for line in lines:
            if not line.startswith("- "):
                is_unordered_list = False
                break

        if is_unordered_list:
            return BlockType.ULIST

    if block.startswith("1. "):
        lines = block.split('\n')
        i = 1
        for line in lines:
            expected_prefix = f"{i}. "

            if not line.startswith(expected_prefix):
                return BlockType.PARAGRAPH

            i += 1

        return BlockType.OLIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    textnodes = text_to_textnodes(text)

    htmlnodes = []

    for tn in textnodes:
        htmlnodes.append(text_node_to_html_node(tn))

    return htmlnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.PARAGRAPH:
            lines = block.split("\n")
            text = " ".join(lines)
            p_children = text_to_children(text)
            children.append(ParentNode("p", children=p_children))

        elif btype == BlockType.HEADING:
            i = 0
            while i < len(block) and block[i] == "#" and i < 6:
                i += 1
            level = i
            text = block[level + 1 :]
            text = text.strip()
            tag = f"h{level}"
            h_children = text_to_children(text)
            children.append(ParentNode(tag, children=h_children))

        elif btype == BlockType.CODE:
            lines = block.split("\n")
            inner_lines = lines[1:-1]
            inner = "\n".join(inner_lines) + "\n"
            code_html = text_node_to_html_node(TextNode(inner, TextType.TEXT))
            pre_node = ParentNode("pre", children=[ParentNode("code", children=[code_html])])
            children.append(pre_node)

        elif btype == BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = [line.lstrip(">").lstrip(" ") for line in lines]
            text = " ".join(stripped_lines)
            q_children = text_to_children(text)
            children.append(ParentNode("blockquote", children=q_children))

        elif btype == BlockType.ULIST:
            li_nodes = []
            for line in block.split("\n"):
                item_text = line[2:]
                li_children = text_to_children(item_text)
                li_nodes.append(ParentNode("li", children=li_children))
            children.append(ParentNode("ul", children=li_nodes))

        elif btype == BlockType.OLIST:
            li_nodes = []
            for line in block.split("\n"):
                dot_index = line.find(". ")
                item_text = line[dot_index + 2 :]
                li_children = text_to_children(item_text)
                li_nodes.append(ParentNode("li", children=li_children))
            children.append(ParentNode("ol", children=li_nodes))

    return ParentNode("div", children=children)
