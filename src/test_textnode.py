import unittest

from textnode import TextNode
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", "bold")
    node2 = TextNode("This is a text node", "bold")
    self.assertEqual(node, node2)
  
  def test_not_equal(self):
    node3 = TextNode("This is an italized link", "italics", "https://www.google.com")
    node4 = TextNode("This is a bold word", "bold")
    self.assertNotEqual(node3, node4)

  def test_conversion(self):
    node = TextNode("display picture", "image", "https://www.google.com")
    leaf_node = LeafNode(
      "img",
      "",
      {
        "src": "https://www.google.com",
        "alt": "display picture"
      }
    )

    self.assertEqual(
      node.text_node_to_html_node().to_html(),
      leaf_node.to_html()
    )
  
  def test_wrong_text_type_conversion(self):
    node = TextNode("display picture", "photo", "https://www.google.com")

    self.assertRaises(ValueError, node.text_node_to_html_node)

if __name__ == "__main__":
  unittest.main()