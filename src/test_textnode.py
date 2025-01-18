import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_repr(self):
       node = TextNode("this is a text node", TextType.BOLD, "www.test.com")
       self.assertEqual("TextNode(this is a text node, TextType.BOLD, www.test.com)", str(node))

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_to_html_node_text(self):
        tnode = TextNode("this was a text node", TextType.NORMAL)
        self.assertEqual(str(text_node_to_html_node(tnode)), str(LeafNode(None, "this was a text node", None)) )
    def test_to_html_node_bold(self):
        tnode = TextNode("this was a text node", TextType.BOLD)
        self.assertEqual(str(text_node_to_html_node(tnode)), str(LeafNode("b", "this was a text node", None)) )
    def test_to_html_node_link(self):
        tnode = TextNode("this was a text node", TextType.LINKS, "www.test.com")
        self.assertEqual(str(text_node_to_html_node(tnode)), str(LeafNode("a", "this was a text node", {"href": "www.test.com"})) )
    def test_to_html_node_image(self):
        tnode = TextNode("this was a text node", TextType.IMAGES, "www.test.com")
        self.assertEqual(str(text_node_to_html_node(tnode)), str(LeafNode("img", "", {"src": "www.test.com","alt":"this was a text node"})) )
    def test_to_html_node_base_case(self):
        with self.assertRaises(Exception):
            text_node_to_html_node(TextNode("this was a text node", TextType.Bullshit, "www.test.com"))

    

if __name__ == "__main__":
    unittest.main()
