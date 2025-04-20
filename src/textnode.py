from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or old_node.text.count(delimiter) == 0:
            new_nodes.append(old_node)
        else:
            if old_node.text.count(delimiter) == 2:
                split_texts = old_node.text.split(delimiter)
                for i in range(0, len(split_texts)):
                    if i == 1:
                        new_node = TextNode(split_texts[i], text_type)
                    else:
                        new_node = TextNode(split_texts[i], TextType.TEXT)
                    new_nodes.append(new_node)
            if old_node.text.count(delimiter) == 1:
                raise Exception("invalid markdown syntax")
    return new_nodes