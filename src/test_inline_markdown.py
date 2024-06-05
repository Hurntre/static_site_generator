import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TestSplitDelimiter(unittest.TestCase):
  def test_delim_code(self):
    node = TextNode("This is text with a `code block` word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "`", text_type_code)

    self.assertEqual(new_nodes, [
      TextNode("This is text with a ", text_type_text),
      TextNode("code block", text_type_code),
      TextNode(" word", text_type_text),
    ])

  def test_delim_italic(self):
    node = TextNode("This is text with an *italicized* word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "*", text_type_italic)

    self.assertEqual(new_nodes, [
      TextNode("This is text with an ", text_type_text),
      TextNode("italicized", text_type_italic),
      TextNode(" word", text_type_text),
    ])

  def test_delim_bold(self):
    node = TextNode("This is text with a **bolded** word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "**", text_type_bold)

    self.assertEqual(new_nodes, [
      TextNode("This is text with a ", text_type_text),
      TextNode("bolded", text_type_bold),
      TextNode(" word", text_type_text),
    ])

  def test_delim_bold_multiword(self):
      node = TextNode("This is text with a **bolded word** and **another**", text_type_text)
      new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
      self.assertListEqual(
          [
              TextNode("This is text with a ", text_type_text),
              TextNode("bolded word", text_type_bold),
              TextNode(" and ", text_type_text),
              TextNode("another", text_type_bold),
          ],
          new_nodes,
      )
  
  def test_not_text_node_output(self):
    node = TextNode("This is italized", text_type_italic)
    new_nodes = split_nodes_delimiter([node], "*", text_type_italic)

    self.assertEqual(new_nodes, [
      TextNode("This is italized", text_type_italic),
    ])
  
  def test_missing_closing_delimiter_error(self):
    node = TextNode("This is text with a `code block word", text_type_text)
    
    with self.assertRaises(Exception) as exc_info:
      split_nodes_delimiter([node], "`", text_type_code)

    self.assertEqual(str(exc_info.exception), "Invalid markdown, formatted section not closed")

  def test_image_extract(self):
    self.assertEqual(
      extract_markdown_images("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"),
      [('image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'), ('another', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png')]         
    )

  def test_link_extract(self):
    self.assertEqual(
      extract_markdown_links("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"),
      [('link', 'https://www.example.com'), ('another', 'https://www.example.com/another')]      
    )
    
  def test_1_image_node_split_without_suffix(self):
    node = TextNode(
      "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
      text_type_text
    )
    new_nodes = split_nodes_image([node])

    self.assertEqual(new_nodes, [
      TextNode("This is text with an ", text_type_text),
      TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    ])

  def test_1_image_node_split_with_suffix(self):
    node = TextNode(
      "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) with suffix",
      text_type_text
    )
    new_nodes = split_nodes_image([node])

    self.assertEqual(new_nodes, [
      TextNode("This is text with an ", text_type_text),
      TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" with suffix", text_type_text),
    ])
  
  def test_split_2_node_image(self):
    node = TextNode(
      "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
      text_type_text
    )
    new_nodes = split_nodes_image([node])

    self.assertEqual(new_nodes, [
      TextNode("This is text with an ", text_type_text),
      TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" and another ", text_type_text),
      TextNode(
        "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
      ),
    ])

  def test_split_3_node_image(self):
    node = TextNode(
      "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and another ![third image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
      text_type_text
    )
    new_nodes = split_nodes_image([node])

    self.assertEqual(new_nodes, [
      TextNode("This is text with an ", text_type_text),
      TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" and another ", text_type_text),
      TextNode(
        "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
      ),
      TextNode(" and another ", text_type_text),
      TextNode(
        "third image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
      ),
    ])

  def test_1_link_node_split_without_suffix(self):
    node = TextNode(
      "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
      text_type_text
    )
    new_nodes = split_nodes_link([node])

    self.assertEqual(new_nodes, [
      TextNode("This is text with an ", text_type_text),
      TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    ])

  def test_1_link_node_split_with_suffix(self):
    node = TextNode(
      "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) with suffix",
      text_type_text
    )
    new_nodes = split_nodes_link([node])

    self.assertEqual(new_nodes, [
      TextNode("This is text with an ", text_type_text),
      TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" with suffix", text_type_text),
    ])
  
  def test_split_2_node_link(self):
    node = TextNode(
      "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
      text_type_text
    )
    new_nodes = split_nodes_link([node])

    self.assertEqual(new_nodes, [
      TextNode("This is text with an ", text_type_text),
      TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" and another ", text_type_text),
      TextNode(
        "second link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
      ),
    ])

  def test_split_3_node_link(self):
    node = TextNode(
      "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and another [third link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
      text_type_text
    )
    new_nodes = split_nodes_link([node])

    self.assertEqual(new_nodes, [
      TextNode("This is text with an ", text_type_text),
      TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" and another ", text_type_text),
      TextNode(
        "second link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
      ),
      TextNode(" and another ", text_type_text),
      TextNode(
        "third link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
      ),
    ])
  
  def test_text_to_textnodes(self):
    nodes = text_to_textnodes('This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)')

    self.assertListEqual(nodes, [
      TextNode("This is ", text_type_text),
      TextNode("text", text_type_bold),
      TextNode(" with an ", text_type_text),
      TextNode("italic", text_type_italic),
      TextNode(" word and a ", text_type_text),
      TextNode("code block", text_type_code),
      TextNode(" and an ", text_type_text),
      TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" and a ", text_type_text),
      TextNode("link", text_type_link, "https://boot.dev"),
    ])

if __name__ == "__main__":
  unittest.main()