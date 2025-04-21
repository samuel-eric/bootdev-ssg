from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or old_node.text.count(delimiter) == 0:
            new_nodes.append(old_node)
        else:
            split_texts = old_node.text.split(delimiter)
            if len(split_texts) % 2 != 0:
                for i in range(0, len(split_texts)):
                    if split_texts[i] == "":
                        continue
                    if i % 2 == 0:
                        new_node = TextNode(split_texts[i], TextType.TEXT)
                    else:
                        new_node = TextNode(split_texts[i], text_type)
                    new_nodes.append(new_node)
            else:
                raise Exception("invalid markdown syntax")
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) > 0:
            for i in range(0, len(images)):
                image_alt, image_link = images[i]
                section_texts = original_text.split(f"![{image_alt}]({image_link})", 1)
                if section_texts[0] != "":
                    new_nodes.append(TextNode(section_texts[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if i != len(images) - 1:
                    original_text = section_texts[1]
                elif section_texts[1] != "":
                    new_nodes.append(TextNode(section_texts[1], TextType.TEXT))

        else:
            new_nodes.append(old_node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) > 0:
            for i in range(0, len(links)):
                link_text, link_url = links[i]
                section_texts = original_text.split(f"[{link_text}]({link_url})", 1)
                if section_texts[0] != "":
                    new_nodes.append(TextNode(section_texts[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                if i != len(links) - 1:
                    original_text = section_texts[1]
                elif section_texts[1] != "":
                    new_nodes.append(TextNode(section_texts[1], TextType.TEXT))

        else:
            new_nodes.append(old_node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes