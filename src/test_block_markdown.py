import unittest

from block_markdown import markdown_to_blocks

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

if __name__ == "__main__":
  unittest.main()