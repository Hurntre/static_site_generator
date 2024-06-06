import os
from pathlib import Path
from block_markdown import markdown_to_blocks, markdown_to_html_node

def extract_title(markdown):
  blocks = markdown_to_blocks(markdown)

  for block in blocks:
    if block.startswith("# "):
      return block.replace("# ", "")
  raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")

  markdown_file = open(from_path, 'r')
  markdown_content = markdown_file.read()
  markdown_file.close()

  template_file = open(template_path, 'r')
  template = template_file.read()
  template_file.close()

  html_node = markdown_to_html_node(markdown_content)
  html = html_node.to_html()

  title = extract_title(markdown_content)
  template = template.replace("{{ Title }}", title)
  template = template.replace("{{ Content }}", html)

  # if not os.path.exists(dest_path):
  #   os.makedirs(dest_path)

  # file_path = os.path.join(dest_path, "index.html")


  dest_dir_path = os.path.dirname(dest_path)
  if dest_dir_path != "":
    os.makedirs(dest_dir_path, exist_ok=True)
  

  with open(dest_path, 'w') as file:
    file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  if not os.path.exists(dest_dir_path):
    os.mkdir(dest_dir_path)

  for filename in os.listdir(dir_path_content):
    from_path = os.path.join(dir_path_content, filename)
    dest_path = os.path.join(dest_dir_path, filename)

    if os.path.isfile(from_path):
      dest_path = Path(dest_path).with_suffix(".html")
      generate_page(from_path, template_path, dest_path)
    else:
      generate_pages_recursive(from_path, template_path, dest_path)