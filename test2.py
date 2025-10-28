import mistune
import subprocess

# Read Markdown text
with open("formatted_output.md", "r", encoding="utf-8") as f:
    markdown_text = f.read()


# ✅ Custom renderer compatible with Mistune ≥3.x
class LatexRenderer(mistune.HTMLRenderer):
    def paragraph(self, text):
        return text + "\n\n"

    def heading(self, text, level):
        if level == 1:
            return f"\\section{{{text}}}\n"
        elif level == 2:
            return f"\\subsection{{{text}}}\n"
        else:
            return f"\\subsubsection{{{text}}}\n"

    def list_item(self, text, level=None):
        # `level` arg is optional depending on Mistune version
        return f"\\item {text}\n"

    def list(self, text, ordered, level, start=None):
        env = "enumerate" if ordered else "itemize"
        return f"\\begin{{{env}}}\n{text}\\end{{{env}}}\n"

    def block_quote(self, text):
        return f"\\begin{{quote}}\n{text}\\end{{quote}}\n"

    def inline_math(self, text):
        return f"${text}$"

    def block_math(self, text):
        return f"\\[{text}\\]"

    def emphasis(self, text):
        return f"\\textit{{{text}}}"

    def strong(self, text):
        return f"\\textbf{{{text}}}"


# Create parser
renderer = LatexRenderer()
markdown = mistune.create_markdown(renderer=renderer, plugins=["strikethrough", "table"])
latex_body = markdown(markdown_text)

# Wrap in LaTeX document
latex_doc = f"""
\\documentclass[12pt]{{article}}
\\usepackage{{amsmath, amssymb}}
\\usepackage{{geometry}}
\\geometry{{margin=1in}}
\\begin{{document}}
{latex_body}
\\end{{document}}
"""

# Save .tex
with open("output.tex", "w", encoding="utf-8") as f:
    f.write(latex_doc)
print("✅ LaTeX file created: output.tex")

# Compile to PDF using MiKTeX / TeX Live
subprocess.run(["pdflatex", "output.tex"], check=True)
# Compile to PDF using MiKTeX / TeX Live
subprocess.run(["pdflatex", "output.tex"], check=True)
print("✅ PDF successfully generated as output.pdf")
