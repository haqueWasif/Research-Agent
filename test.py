import re

def format_llm_to_markdown(input_text: str) -> str:
    """
    Converts raw LLM output into clean Markdown + LaTeX format.
    """

    md_text = input_text

    # 1. Remove extraneous '#' symbols not used as headings
    md_text = re.sub(r'(?<!\n)#+(?! )', '', md_text)

    # 2. Ensure headings have space after '#' symbols
    md_text = re.sub(r'^(#+)([^\s#])', r'\1 \2', md_text, flags=re.MULTILINE)

    # 3. Fix nested lists: add 2 spaces for sub-items if needed
    # Match '-' or '*' at start of line preceded by spaces
    lines = md_text.split('\n')
    formatted_lines = []
    for line in lines:
        # Indent lines with nested bullet points (sub-bullets)
        if re.match(r'^\s*-\s+', line):
            formatted_lines.append(line)
        elif re.match(r'^\s{2,}-\s+', line):
            formatted_lines.append('  ' + line.strip())
        else:
            formatted_lines.append(line)
    md_text = '\n'.join(formatted_lines)

    # 4. Ensure all equations in $...$ or $$...$$ stay intact (no changes)
    # Already inline or block, so we don't modify

    # 5. Optional: add extra line breaks before headers for better PDF formatting
    md_text = re.sub(r'\n(#+)', r'\n\n\1', md_text)

    return md_text


if __name__ == "__main__":
    # Load your LLM output
    with open("Research_Agent_ML_Note.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()

    formatted_md = format_llm_to_markdown(raw_text)

    # Save to Markdown file
    with open("formatted_output.md", "w", encoding="utf-8") as f:
        f.write(formatted_md)

    print("Markdown formatting complete! Saved to formatted_output.md")
