from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("h1", "test paragraph")
        self.assertEqual(str(node), "tag = h1, value = test paragraph, children = None, props = None")

    def test_props_to_html(self):
        node = HTMLNode("h1", "test paragraph", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "testing", None)
        self.assertEqual(node.to_html(), "<p>testing</p>")

    def test_value_error(self):
        node = LeafNode("p", None)
        
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        leaf_node = LeafNode("p", "testing", None)
        parent_node = ParentNode("h", [leaf_node], None)
        self.assertEqual(parent_node.to_html(), "<h><p>testing</p></h>")


    def test_to_html_with_multiple_children(self):
        first_leaf_node = LeafNode("p", "testing", None)
        second_leaf_node = LeafNode(None, "test2", None)
        third_leaf_node = LeafNode("b", "test3", {"bing":"bong"})
        parent_node = ParentNode("h", [first_leaf_node, second_leaf_node, third_leaf_node], None)
        self.assertEqual(parent_node.to_html(), "<h><p>testing</p>test2<b bing=\"bong\">test3</b></h>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )



if __name__ == "__main__":
    unittest.main()
