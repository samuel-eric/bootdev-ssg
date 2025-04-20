from enum import Enum
import re

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
