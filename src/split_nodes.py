from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        split_nodes = []
        split_node_text = node.text.split(delimiter)
        for i in range(0, len(split_node_text)):
            if split_node_text[i] == "":
                continue
            if not i % 2:
                split_nodes.append(TextNode(split_node_text[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(split_node_text[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_images = extract_markdown_images(node.text)
        if not node_images:
            new_nodes.append(node)
            continue
        current_text = node.text
        for alt_text, url in node_images:
            markdown_img = f"![{alt_text}]({url})"
            sections = current_text.split(markdown_img, 1) 
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGES, url))
            
            current_text = sections[1]
        if current_text != '':
            new_nodes.append(TextNode(current_text,TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_links = extract_markdown_links(node.text)
        if not node_links:
            new_nodes.append(node)
            continue
        current_text = node.text
        for alt_text, url in node_links:
            markdown_link= f"[{alt_text}]({url})"
            sections = current_text.split(markdown_link, 1) 
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            
            new_nodes.append(TextNode(alt_text, TextType.LINKS, url))
            
            current_text = sections[1]
        if current_text != '':
            new_nodes.append(TextNode(current_text,TextType.NORMAL))
    return new_nodes

def text_to_textnodes(text):
    delimiters_dict = {"**":TextType.BOLD, "*":TextType.ITALIC, "`":TextType.CODE}
    current_nodes = [TextNode(text, TextType.NORMAL)]
    for key, value in delimiters_dict.items():
        current_nodes = split_nodes_delimiter(current_nodes, key, value)
    current_nodes = split_nodes_image(current_nodes)
    current_nodes = split_nodes_link(current_nodes)
    return current_nodes
