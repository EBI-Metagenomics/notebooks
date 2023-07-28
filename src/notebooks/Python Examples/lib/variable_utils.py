import os
from IPython.display import Markdown

def get_variable_from_link_or_input(variable, name = 'accession', default = None):
    """
    Get a variable value, either from an ENV VAR that would have been set by the jlab_query_paramms extension, or through direct user input.
    """
    var = os.getenv(variable)
    if var:
        display(Markdown(f'<span style="background-color: #0a5032; color: #fff; padding: 8px;">Using {name} <emph>{var}</emph> from the link you followed.</span>'))
    else:
        var = input(f'Type {"an" if name[0].lower() in "aeiou" else "a"} {name} [default: {str(default)}]')
    var = var or default
    print(f'Using "{var}" as {name}')
    return var
