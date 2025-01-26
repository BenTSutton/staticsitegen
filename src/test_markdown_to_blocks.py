import unittest
from markdown_to_blocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_block, get_header_tag
from htmlnode import HTMLNode, ParentNode, LeafNode

class test_markdown_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        self.assertListEqual([
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ], markdown_to_blocks("# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"))
    
    def test_markdown_block_type_heading(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("# bing bong"))

    def test_markdown_block_type_heading_2(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("### bing bong"))

    def test_markdown_block_type_code(self):
        self.assertEqual(BlockType.CODE, block_to_block_type("```python\nthis is some code\n```"))
    
    def test_markdown_block_type_quote(self):
        self.assertEqual(BlockType.QUOTE, block_to_block_type(">this shit rules\n>bing bong"))


    def test_markdown_block_type_not_quote(self):
        self.assertNotEqual(BlockType.QUOTE, block_to_block_type(">this shit rules\nbing bong"))
    def test_markdown_block_type_ordered_list(self):
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type("1. bing\n2. bong"))
    
    def test_get_header_tag(self):
        self.assertEqual(get_header_tag("### test#"), "h3")

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_block(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_block(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

