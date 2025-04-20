import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)

    def test_neq_url(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link node", TextType.LINK, "https://google.com")
        node3 = TextNode("This is a link node", TextType.LINK)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)

    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_split_delimiter_bold(self):
        node1 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node3 = TextNode("This is also a text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is also a text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_split_delimiter_not_text(self):
        node1 = TextNode("This is text with a **bold** word", TextType.BOLD)
        node2 = TextNode("This is also a text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        expected_result = [
            TextNode("This is text with a **bold** word", TextType.BOLD),
            TextNode("This is also a text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

if __name__ == "__main__":
    unittest.main()