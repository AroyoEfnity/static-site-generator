from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    # Check the type of the text_node
    if text_node.text_type == TextType.TEXT:
        # For plain text, return a LeafNode with no tag
        return LeafNode(None, text_node.text)
    
    elif text_node.text_type == TextType.BOLD:
        # For bold text, return a LeafNode with "b" tag
        return LeafNode("b", text_node.text)
    
    elif text_node.text_type == TextType.ITALIC:
        # For italic text, return a LeafNode with "i" tag
        return LeafNode("i", text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        # For code text, return a LeafNode with "code" tag
        return LeafNode("code", text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        # For links, return a LeafNode with "a" tag and "href" prop
        props = {"href": text_node.url}
        return LeafNode("a", text_node.text, props)
    
    elif text_node.text_type == TextType.IMAGE:
        props = {
            "src": text_node.url,  # Assuming your TextNode stores URLs in a url attribute
            "alt": text_node.alt   # Assuming your TextNode stores alt text in an alt attribute
        }
        return LeafNode("img", "", props)  # Note the empty string as the value
    
    else:
        # If we get here, it's an unknown type
        raise ValueError(f"Invalid text type: {text_node.text_type}")