import unittest

from inline_markdown import split_nodes_delimiter, TextType, extract_markdown_images, extract_markdown_links
from textnode import TextNode


class TestSplitDelimiter(unittest.TestCase):
  def test_delim_code(self):
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    self.assertEqual(new_nodes, [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" word", TextType.TEXT),
    ])

  def test_delim_italic(self):
    node = TextNode("This is text with an *italicized* word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

    self.assertEqual(new_nodes, [
      TextNode("This is text with an ", TextType.TEXT),
      TextNode("italicized", TextType.ITALIC),
      TextNode(" word", TextType.TEXT),
    ])

  def test_delim_bold(self):
    node = TextNode("This is text with a **bolded** word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    self.assertEqual(new_nodes, [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("bolded", TextType.BOLD),
      TextNode(" word", TextType.TEXT),
    ])

  def test_delim_bold_multiword(self):
      node = TextNode("This is text with a **bolded word** and **another**", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
      self.assertListEqual(
          [
              TextNode("This is text with a ", TextType.TEXT),
              TextNode("bolded word", TextType.BOLD),
              TextNode(" and ", TextType.TEXT),
              TextNode("another", TextType.BOLD),
          ],
          new_nodes,
      )
  
  def test_not_text_node_output(self):
    node = TextNode("This is italized", TextType.ITALIC)
    new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

    self.assertEqual(new_nodes, [
      TextNode("This is italized", TextType.ITALIC),
    ])
  
  def test_missing_closing_delimiter_error(self):
    node = TextNode("This is text with a `code block word", TextType.TEXT)
    
    with self.assertRaises(Exception) as exc_info:
      split_nodes_delimiter([node], "`", TextType.CODE)

    self.assertEqual(str(exc_info.exception), "Invalid markdown syntax")

  def test_missing_closing_delimiter_error(self):
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    
    with self.assertRaises(Exception) as exc_info:
      split_nodes_delimiter([node], "`", "CODEC")

    self.assertEqual(str(exc_info.exception), "Invalid text type provided")

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