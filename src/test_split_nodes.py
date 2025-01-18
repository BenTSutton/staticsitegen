from split_nodes import *
import unittest

class test_split_nodes(unittest.TestCase):
    def test_hidden_bolds(self):
        nodes = [TextNode("finding a *bold* character", TextType.NORMAL)]
        first = TextNode("finding a ", TextType.NORMAL)
        second = TextNode("bold", TextType.BOLD)
        third = TextNode(" character", TextType.NORMAL)
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), [first, second, third])

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
    
    def test_extract_images(self):
        self.assertEqual([('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')], extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"))
    
    def test_extract_links(self):
        self.assertEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"))       

    def test_split_images(self):
        self.assertEqual([
            TextNode("this ", TextType.NORMAL),
            TextNode("image", TextType.IMAGES, "www.test.com"),
            TextNode(" worked", TextType.NORMAL)
        ], split_nodes_image([
            TextNode("this ![image](www.test.com) worked", TextType.NORMAL)
        ]))

    def test_text_to_new_nodes(self):
        self.assertListEqual(
            text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        ,[
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINKS, "https://boot.dev"),
        ]
        )