import unittest

from block import *

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks_1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here

This is the new paragraph on a new line

- This is a list

- This is another list
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here",
                "This is the new paragraph on a new line",
                "- This is a list",
                "- This is another list"
            ],
        )

    def test_block_to_block_type_unordered_list(self):
        md = "- This is a list\n- This is another list"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_heading(self):
        md = "#### heading 4"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_block_to_block_type_paragraph(self):
        md = ">this is quote\n- this is list"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code(self):
        md = "```this is code```"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )

    def test_block_to_block_type_ordered_list_1(self):
        md = "1. this is quote\n2. this is list"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_ordered_list_2(self):
        md = "1. this is quote\n2.this is list"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

if __name__ == "__main__":
    unittest.main()