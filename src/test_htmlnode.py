import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
  def test_value(self):
    link_node = HTMLNode(
      "a", 
      "google",
      None,
      {
        "href": "https://www.google.com",
        "class": "links" 
      }
    )
    self.assertEqual(
      link_node.props_to_html(),
      ' href="https://www.google.com" class="links"'
    )

    self.assertEqual(
      link_node.__repr__(),
      "HTMLNode(a, google, None, {'href': 'https://www.google.com', 'class': 'links'})"
    )

  def test_paragraph_leaf_node(self):
    node = LeafNode("p", "This is a paragraph of text.")
    self.assertEqual(node.to_html(),'<p>This is a paragraph of text.</p>')

  def test_link_leaf_node(self):
    node = LeafNode(
      "a",
      "Click me!",
      {"href": "https://www.google.com"}
    )

    self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
  

  def test_headings(self):
    node = ParentNode(
      "h2",
      [
          LeafNode("b", "Bold text"),
          LeafNode(None, "Normal text"),
          LeafNode("i", "italic text"),
          LeafNode(None, "Normal text"),
	    ]
    )
    
    self.assertEqual(
         node.to_html(),
         "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>"
		)
    
  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
      parent_node.to_html(),
      "<div><span><b>grandchild</b></span></div>",
    )
  
if __name__ == "__main__":
  unittest.main()