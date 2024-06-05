import re

def markdown_to_blocks(markdown):
  splitted_blocks = markdown.split("\n\n")
  filtered_blocks = list(filter(lambda block: block != "", splitted_blocks))
  stripped_blocks = list(map(lambda block: block.strip(), filtered_blocks))

  return stripped_blocks
  