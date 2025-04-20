def markdown_to_blocks(markdown):
    lines = list(filter(lambda line: line != "",map(lambda line: line.strip(),markdown.split("\n\n"))))
    return lines