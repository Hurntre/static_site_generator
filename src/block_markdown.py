from enum import Enum
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes

class BlockType(Enum):
  PARAGRAPH = 'paragraph'
  HEADING = 'heading'
  CODE = 'code'
  QUOTE = 'quote'
  ULIST = 'unordered_list'
  OLIST = 'ordered_list'

def markdown_to_blocks(markdown):
  splitted_blocks = markdown.split("\n\n")
  filtered_blocks = list(filter(lambda block: block != "", splitted_blocks))
  stripped_blocks = list(map(lambda block: block.strip(), filtered_blocks))

  return stripped_blocks

def block_to_block_type(block):
  lines = block.split("\n")

  if (
      block.startswith("# ")
      or block.startswith("## ")
      or block.startswith("### ")
      or block.startswith("#### ")
      or block.startswith("##### ")
      or block.startswith("###### ")
  ):
      return BlockType.HEADING
  
  if (
    len(lines) > 1
    and lines[0].startswith("```")
    and lines[-1].startswith("```")
  ) or (
    block.startswith("```")
    and block.endswith("```")
  ):
    return BlockType.CODE
  
  if block.startswith(">"):
    for line in lines:
      if not line.startswith(">"):
        return BlockType.PARAGRAPH
    return BlockType.QUOTE
  if block.startswith("* "):
    for line in lines:
      if not line.startswith("* "):
        return BlockType.PARAGRAPH
    return BlockType.ULIST
  if block.startswith("- "):
    for line in lines:
      if not line.startswith("- "):
        return BlockType.PARAGRAPH
    return BlockType.ULIST
  if block.startswith("1. "):
    i = 1
    for line in lines:
      if not line.startswith(f"{i}. "):
        return BlockType.PARAGRAPH
      i += 1
    return BlockType.OLIST
  return BlockType.PARAGRAPH

def paragraph_html_node(block):
  inline_text_nodes = text_to_textnodes(block)
  inline_leaf_nodes = []

  for inline_text_node in inline_text_nodes:
    inline_leaf_nodes.append(inline_text_node.text_node_to_html_node())
  
  return ParentNode("p", inline_leaf_nodes)

def heading_html_node(block):    
  if block.startswith("# "):
    return LeafNode("h1", block.replace("# ", ""))
  if block.startswith("## "):
    return LeafNode("h2", block.replace("## ", ""))
  if block.startswith("### "):
    return LeafNode("h3", block.replace("### ", ""))
  if block.startswith("#### "):
    return LeafNode("h4", block.replace("#### ", ""))
  if block.startswith("##### "):
    return LeafNode("h5", block.replace("##### ", ""))
  if block.startswith("###### "):
    return LeafNode("h6", block.replace("###### ", ""))

def code_html_node(block):
  return ParentNode("code",[LeafNode("pre", block)])

def olist_html_node(block):
  list_items =  block.split("\n")
  formatted_items = []

  i = 1
  for list_item in list_items:
    formatted_items.append(list_item.replace(f"{i}. ", ""))
    i += 1
  
  list_items_nodes = []
  for item in formatted_items:
    list_items_nodes.append(LeafNode("li", item))

  return ParentNode("ol", list_items_nodes)

def ulist_html_node(block):
  list_items =  block.split("\n")
  formatted_items = []

  if block.startswith("* "):
    for list_item in list_items:
      formatted_items.append(list_item.replace("* ", ""))
    
  if block.startswith("- "):
    for list_item in list_items:
      formatted_items.append(list_item.replace("- ", ""))
  
  list_items_nodes = []
  for item in formatted_items:
    list_items_nodes.append(LeafNode("li", item))

  return ParentNode("ul", list_items_nodes)

def quote_html_node(block):
  return LeafNode("blockquote", block.replace(">", ""))

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)

  block_nodes = []

  for block in blocks:
    block_type = block_to_block_type(block)

    if block_type is BlockType.PARAGRAPH:
      block_nodes.append(paragraph_html_node(block))
    if block_type is BlockType.HEADING:
      block_nodes.append(heading_html_node(block))
    if block_type is BlockType.CODE:
      block_nodes.append(code_html_node(block))
    if block_type is BlockType.QUOTE:
      block_nodes.append(quote_html_node(block))
    if block_type is BlockType.ULIST:
      block_nodes.append(ulist_html_node(block))
    if block_type is BlockType.OLIST:
      block_nodes.append(olist_html_node(block))
    
  return ParentNode("div", block_nodes)