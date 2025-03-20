import unittest
from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Add similar assertions as above
    
    def test_italic_delimiter(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        # Add assertions
    
    def test_multiple_delimiter_pairs(self):
        node = TextNode("This has `one code` and `another code` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Add assertions to verify 5 nodes: text, code, text, code, text
    
def test_no_delimiter(self):
    node = TextNode("This is text with no delimiters", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    self.assertEqual(len(new_nodes), 1)
    self.assertEqual(new_nodes[0].text, "This is text with no delimiters")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

def test_multiple_nodes(self):
    node1 = TextNode("This is text", TextType.TEXT)
    node2 = TextNode("This is `code`", TextType.TEXT)
    node3 = TextNode("This is bold", TextType.BOLD)  # Non-TEXT type should be left as-is
    
    new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
    
    self.assertEqual(len(new_nodes), 4)
    self.assertEqual(new_nodes[2].text, "code")
    self.assertEqual(new_nodes[2].text_type, TextType.CODE)
    self.assertEqual(new_nodes[3].text, "This is bold")
    self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

def test_missing_closing_delimiter(self):
    node = TextNode("This has `code without closing", TextType.TEXT)
    
    with self.assertRaises(ValueError):
        split_nodes_delimiter([node], "`", TextType.CODE)

def test_split_nodes_image_basic(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

def test_split_nodes_image_no_images(self):
    node = TextNode("This is text with no images", TextType.TEXT)
    new_nodes = split_nodes_image([node])
    self.assertListEqual([node], new_nodes)

def test_split_nodes_image_non_text_node(self):
    node = TextNode("image alt", TextType.IMAGE, "https://example.com/image.png")
    new_nodes = split_nodes_image([node])
    self.assertListEqual([node], new_nodes)

def test_split_nodes_image_multiple_nodes(self):
    nodes = [
        TextNode("Text with ![image](https://example.com/img.png)", TextType.TEXT),
        TextNode("No image here", TextType.TEXT),
        TextNode("Another ![pic](https://example.com/pic.jpg)", TextType.TEXT),
    ]
    new_nodes = split_nodes_image(nodes)
    self.assertListEqual(
        [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode("No image here", TextType.TEXT),
            TextNode("Another ", TextType.TEXT),
            TextNode("pic", TextType.IMAGE, "https://example.com/pic.jpg"),
        ],
        new_nodes,
    )

def test_split_nodes_link_basic(self):
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ],
        new_nodes,
    )

def test_split_nodes_link_no_links(self):
    node = TextNode("This is text with no links", TextType.TEXT)
    new_nodes = split_nodes_link

if __name__ == "__main__":
    unittest.main()
