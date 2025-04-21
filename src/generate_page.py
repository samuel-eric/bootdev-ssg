from markdown_block import markdown_to_html_node, extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path)
    markdown = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path)
    template = template_file.read()
    template_file.close()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    result_html = ""
    result_html = template.replace("{{ Content }}", html)
    result_html = result_html.replace("{{ Title }}", title)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, 'x') as f:
        f.write(result_html)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for object in os.listdir(dir_path_content):
        content_filepath = os.path.join(dir_path_content, object)
        dest_filepath = os.path.join(dest_dir_path, object)
        if os.path.isfile(content_filepath) and content_filepath[-2:] == "md":
            dest_filepath = dest_filepath.replace(".md", ".html")
            generate_page(content_filepath, template_path, dest_filepath)
        else:
            generate_page_recursive(content_filepath, template_path, dest_filepath)