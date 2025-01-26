from enum import Enum
from htmlnode import *
from split_nodes import text_to_textnodes
from textnode import text_node_to_html_node, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    sentences = markdown.split("\n\n")
    for sentence in sentences:
        if sentence == "":
            continue
        blocks.append(sentence.strip())
    return blocks

def block_to_block_type(markdown):
    headings = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
    if markdown.startswith(tuple(headings)):
        return BlockType.HEADING
    if markdown[:3] == "```" and markdown[-3:] == "```":
        return BlockType.CODE
    lines = markdown.split("\n")
    if lines[0][0] == ">":
        matching = True
        for line in lines:
            if line[0] != ">":
                matching = False
                break
        if matching:
            return BlockType.QUOTE
    if lines[0][:2] == "- " or lines[0][:2] == "* ":
        matching = True
        for line in lines:
            if line[:2] != "- " and line[:2] != "* ":
                matching = False
                break
        if matching:
            return BlockType.UNORDERED_LIST
    
    if lines[0][:3] == "1. ":
        matching = True
        for i in range(1, len(lines)):
            if lines[i][:3] != f"{i + 1}. ":
                matching = False
                break
        if matching:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def get_header_tag(block):
    headings = block.split(" ")
    return f"h{headings[0].count('#')}"

def get_child_list_nodes(block, tag):
    nodes = []
    list_items = block.split("\n")
    if tag == "ul":
        start = 2
    if tag == "ol":
        start = 3
    
    for item in list_items:
        text = item[start:]
        child_nodes = text_to_html_nodes(text)
        nodes.append(ParentNode("li", child_nodes))
    return ParentNode(tag, nodes)

def text_to_html_nodes(text):
    block_html_nodes = []
    block_text_nodes = text_to_textnodes(text)
    for txtblock in block_text_nodes:
        child = text_node_to_html_node(txtblock) 
        block_html_nodes.append(child)
    return block_html_nodes

def markdown_to_html_block(md):
    blocks = markdown_to_blocks(md)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH: 
            lines = block.split("\n")
            paragraph = " ".join(lines)
            child_nodes = text_to_html_nodes(paragraph)
            nodes.append(ParentNode("p", child_nodes))
            continue

        if block_type == BlockType.HEADING:
            tag = get_header_tag(block)
            nodes.append(ParentNode(tag, block))
            continue

        if block_type == BlockType.CODE:
            text = block[4:-3]
            child_nodes =  text_to_html_nodes(text)
            nodes.append(ParentNode("pre", LeafNode("code", text)))
            continue

        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.lstrip(">").strip())
            paragraph = " ".join(new_lines)
            child_nodes = text_to_html_nodes()
            nodes.append(LeafNode("blockquote", child_nodes))
            continue

        if block_type == BlockType.UNORDERED_LIST:
            nodes.append(get_child_list_nodes(block, "ul"))
            continue

        if block_type == BlockType.ORDERED_LIST:
            nodes.append(get_child_list_nodes(block, "ol"))
            continue

    return ParentNode("div", nodes)


