class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return_string = ""
        for item in self.props:
            return_string += f" {item}=\"{self.props[item]}\""
        return return_string

    def __repr__(self):
        return f"tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, prop=None):
        super().__init__(tag, value, None, prop)

    def to_html(self):
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value
        prop_text = self.props_to_html()
        return f"<{self.tag}{prop_text}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("requires a tag")
        if self.children is None:
            raise ValueError("node requires children")
        return_string = ""
        for child in self.children:
            return_string += child.to_html()
        return f"<{self.tag}>{return_string}</{self.tag}>"
