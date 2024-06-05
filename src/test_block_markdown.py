import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestSplitDelimiter(unittest.TestCase):
  def test_markdown_to_blocks(self):
    markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item"""
    blocks = markdown_to_blocks(markdown)
    self.assertEqual(
      blocks,
      [
        "# This is a heading",
        "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        "* This is a list item\n* This is another list item",
      ],
    )

  def test_markdown_to_blocks_2(self):
    markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
    blocks = markdown_to_blocks(markdown)
    self.assertEqual(
      blocks,
      [
        "This is **bolded** paragraph",
        "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
        "* This is a list\n* with items",
      ],
    )
  
  def test_paragraph_block_to_block_type(self):
    block_type = block_to_block_type("This is **bolded** paragraph")

    self.assertEqual(block_type, BlockType.PARAGRAPH)

  def test_code1_block_to_block_type(self):
    block_type = block_to_block_type("```This is a code paragraph```")

    self.assertEqual(block_type, BlockType.CODE)

  def test_code_block_to_block_type(self):
    block_type = block_to_block_type("```\nThis is a code paragraph\n```")

    self.assertEqual(block_type, BlockType.CODE)

  def test_ulist_block_to_block_type(self):
    block_type = block_to_block_type("* This is a list\n* with items")

    self.assertEqual(block_type, BlockType.ULIST)

  def test_ulist_block_to_block_type(self):
    block_type = block_to_block_type("- This is a list\n- with items")

    self.assertEqual(block_type, BlockType.ULIST)

  def test_invalid_ulist_block_to_block_type(self):
    block_type = block_to_block_type("- This is a list\n* with items")

    self.assertEqual(block_type, BlockType.PARAGRAPH)

  def test_olist_block_to_block_type(self):
    block_type = block_to_block_type("1. This is a list\n2. with items")

    self.assertEqual(block_type, BlockType.OLIST)

  def test_quote_block_to_block_type(self):
    block_type = block_to_block_type(">This is a list\n>with items")

    self.assertEqual(block_type, BlockType.QUOTE)

  def test_heading1_block_to_block_type(self):
    block_type = block_to_block_type("# This is a heading")

    self.assertEqual(block_type, BlockType.HEADING)
  
  def test_heading2_block_to_block_type(self):
    block_type = block_to_block_type("## This is a heading")

    self.assertEqual(block_type, BlockType.HEADING)
  
  def test_heading3_block_to_block_type(self):
    block_type = block_to_block_type("### This is a heading")

    self.assertEqual(block_type, BlockType.HEADING)
  
  def test_heading4_block_to_block_type(self):
    block_type = block_to_block_type("#### This is a heading")

    self.assertEqual(block_type, BlockType.HEADING)

  def test_heading5_block_to_block_type(self):
    block_type = block_to_block_type("##### This is a heading")

    self.assertEqual(block_type, BlockType.HEADING)

  def test_heading6_block_to_block_type(self):
    block_type = block_to_block_type("###### This is a heading")

    self.assertEqual(block_type, BlockType.HEADING)
  
  def test_heading7_block_to_block_type(self):
    block_type = block_to_block_type("####### This is not a heading")

    self.assertEqual(block_type, BlockType.PARAGRAPH)

  def test_markdown_to_html_node(self):
    markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item"""
    node = markdown_to_html_node(markdown)
    self.assertEqual(
      node.to_html(),
      "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is a list item</li><li>This is another list item</li></ul></div>"
    )

if __name__ == "__main__":
  unittest.main()