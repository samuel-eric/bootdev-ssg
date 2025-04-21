from enum import Enum
import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    lines = list(filter(lambda line: line != "",map(lambda line: line.strip(),markdown.split("\n\n"))))
    return lines

def block_to_block_type(block):
    lines = block.split("\n")
    block_type = ""
    for i in range(0, len(lines)):
        if re.search(r"\#{1,6} .*", lines[i]):
            block_type = BlockType.HEADING
        elif re.search(r"\`\`\`\n|.*?\`\`\`", lines[i]):
            block_type = BlockType.CODE
        elif re.search(r"\>.*", lines[i]):
            if block_type != "" and block_type != BlockType.QUOTE:
                block_type = BlockType.PARAGRAPH
            else:
                block_type = BlockType.QUOTE
        elif re.search(r"\- .*", lines[i]):
            if block_type != "" and block_type != BlockType.UNORDERED_LIST:
                block_type = BlockType.PARAGRAPH
            else:
                block_type = BlockType.UNORDERED_LIST
        elif re.search(r"\d+\. .*", lines[i]):
            if block_type != "" and block_type != BlockType.ORDERED_LIST:
                block_type = BlockType.PARAGRAPH
            else:
                number = int(re.findall(r"(\d+)\. .*", lines[i])[0]) - 1
                if number == i:
                    block_type = BlockType.ORDERED_LIST
                else:
                    block_type = BlockType.PARAGRAPH
        else:
            block_type = BlockType.PARAGRAPH
    return block_type

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        nodes.append(node)
    return ParentNode("div", nodes)

def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            children = text_to_children(text)
            html_node = ParentNode("p", children)
            return html_node
        case BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                new_lines.append(line.lstrip(">").strip())
            text = " ".join(new_lines)
            children = text_to_children(text)
            html_node = ParentNode("blockquote", children)
            return html_node
        case BlockType.HEADING:
            number_hashtag = re.findall(r"(\#{1,6}) .*", block)
            if len(number_hashtag) == 0:
                raise ValueError("invalid heading level")
            level = number_hashtag[0].count("#")
            text = re.findall(r"\#{1,6} (.*)", block)[0]
            children = text_to_children(text)
            html_node = ParentNode(f"h{level}", children)
            return html_node
        case BlockType.UNORDERED_LIST:
            return block_to_list_node(block, BlockType.UNORDERED_LIST)
        case BlockType.ORDERED_LIST:
            return block_to_list_node(block, BlockType.ORDERED_LIST)
        case BlockType.CODE:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("invalid code block")
            text = block[4:-3]
            text_node = TextNode(text, TextType.CODE)
            text_html = text_node_to_html_node(text_node)
            parent = ParentNode("pre", [text_html])
            return parent
        case _:
            raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def block_to_list_node(block, type):
    list_items = block.split("\n")
    list_item_nodes = []
    match type:
        case BlockType.ORDERED_LIST:
            for list_item in list_items:
                text = list_item[3:]
                children = text_to_children(text)
                list_item_node = ParentNode("li", children)
                list_item_nodes.append(list_item_node)
            return ParentNode("ol", list_item_nodes)
        case BlockType.UNORDERED_LIST:
            for list_item in list_items:
                text = list_item[2:]
                children = text_to_children(text)
                list_item_node = ParentNode("li", children)
                list_item_nodes.append(list_item_node)
            return ParentNode("ul", list_item_nodes)
