import sys
import nbformat

# read notebook from stdin
nb = nbformat.reads(sys.stdin.read(), as_version = 4)

# add a quarto callout to the top of notebook, after any raw cells (which probably contain the YAML front matter)

new_cells = nb.cells[:]

for index, cell in enumerate(nb.cells):
  if not cell.cell_type == 'raw':
    cell = nbformat.v4.new_markdown_cell(
      source=""":::{.callout-note}
## This is a static preview
You can run and edit these examples interactively on [Galaxy](https://usegalaxy.eu/root?tool_id=interactive_tool_mgnify_notebook)
:::"""
    )
    new_cells.insert(index, cell)
    break
nb.cells = new_cells

nbformat.write(nb, sys.stdout)
