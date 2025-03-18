from textnode import TextNode, TextType

def main():
    # Create a TextNode with some dummy values
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    
    # Print the node
    print(node)

if __name__ == "__main__":
    main()