import unittest

from textnode import TextNode
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_1(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')

    def test_props_to_html_2(self):
        node = HTMLNode(None, None, None, {"width": 100, "height": 200})
        self.assertEqual(node.props_to_html(), 'width="100" height="200"')

    def test_props_to_html_null(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(node.props_to_html(), '')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is text")
        self.assertEqual(node.to_html(), "This is text")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node_1 = LeafNode("p", "child 1")
        child_node_2 = LeafNode("div", "child 2")
        child_node_3 = LeafNode("span", "child 3")
        child_node_4 = LeafNode("h1", "child 4")
        parent_node = ParentNode("div", [child_node_1, child_node_2, child_node_3, child_node_4])
        self.assertEqual(parent_node.to_html(), "<div><p>child 1</p><div>child 2</div><span>child 3</span><h1>child 4</h1></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_children_props(self):
        child_node = LeafNode("a", "click me!", {"href": "https://www.boot.dev"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><a href="https://www.boot.dev">click me!</a></div>')

    def test_to_html_with_parent_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"width": 400})
        self.assertEqual(parent_node.to_html(), '<div width="400"><span>child</span></div>')

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "http://image-url.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props_to_html(), 'src="http://image-url.com" alt="This is a image node"')

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")