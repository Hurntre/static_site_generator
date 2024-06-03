import re
from textnode import TextNode
from enum import Enum

class TextType(Enum):
  TEXT = "Text"
  BOLD = "Bold"
  ITALIC = "Italic"
  CODE = "Code"
  LINK = "Link"
  IMAGE = "Image"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
  if text_type not in TextType:
    raise Exception("Invalid text type provided")
  new_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      new_nodes.append(old_node)
      continue

    split_nodes = []
    sections = old_node.text.split(delimiter)
    if len(sections) % 2 == 0:
      raise ValueError("Invalid markdown, formatted section not closed")
    for i in range(len(sections)):
      if sections[i] == "":
        continue
      if i % 2 == 0:
        split_nodes.append(TextNode(sections[i], TextType.TEXT))
      else:
        split_nodes.append(TextNode(sections[i], text_type))
    new_nodes.extend(split_nodes)
  return new_nodes

def extract_markdown_images(text):
  pattern = r"!\[(.*?)\]\((.*?)\)"
  matches = re.findall(pattern, text)
  return matches


def extract_markdown_links(text):
  pattern = r"\[(.*?)\]\((.*?)\)"
  matches = re.findall(pattern, text)
  return matches

