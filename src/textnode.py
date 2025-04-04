from enum import Enum
from htmlnode import *

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    match text_type:
        case text_type.NORMAL:
            return LeafNode(None, text_node.text, None)
        case text_type.BOLD:
            return LeafNode("b", text_node.text, None)
        case text_type.ITALIC:
            return LeafNode("i", text_node.text, None)
        case text_type.CODE:
            return LeafNode("code", text_node.text, None)
        case text_type.LINKS:
            return LeafNode("a", text_node.text, {"href": text_node.url}) 
        case text_type.IMAGES:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Invalid texttype")