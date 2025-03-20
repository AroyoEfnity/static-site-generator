from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        text = old_node.text

        if delimiter not in text:
            result.append(old_node)
            continue

        start_index = text.find(delimiter)

        end_index = text.find(delimiter, start_index + len(delimiter))

        if end_index == -1:
            raise ValueError(f"Closing delimiter {delimiter} not found in text: {text}")
        
        before_text = text[:start_index]
        between_text = text[start_index + len(delimiter):end_index]
        after_text = text[end_index + len(delimiter):]

        if before_text:
            result.append(TextNode(before_text, TextType.TEXT))
        
        result.append(TextNode(between_text, text_type))

        if after_text:
            remaining_nodes = split_nodes_delimiter([TextNode(after_text, TextType.TEXT)], delimiter, text_type)
            result.extend(remaining_nodes)

    return result

def split_nodes_link(old_nodes):
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)
        
        if not links:
            result.append(old_node)
            continue
        
        remaining_text = text
        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            parts = remaining_text.split(link_markdown, 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(link_text, TextType.LINK, link_url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
    
    return result

def split_nodes_image(old_nodes):
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)
        
        if not images:
            result.append(old_node)
            continue
        
        remaining_text = text
        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the image node
            result.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Update remaining_text for next iteration
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        # Add any remaining text after the last image
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
    
    return result