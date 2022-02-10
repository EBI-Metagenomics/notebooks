# import os
# from IPython.display import Markdown

# def get_variable_from_link_or_input(variable, name = 'accession', default = None):
#     """
#     Get a variable value, either from an ENV VAR that would have been set by the shiny_proxy_jlab_query_parms extension, or through direct user input.
#     """
#     var = os.getenv(variable)
#     if var:
#         display(Markdown(f'<span style="background-color: #0a5032; color: #fff; padding: 8px;">Using {name} <emph>{var}</emph> from the link you followed.</span>'))
#     else:
#         var = input(f'Type {"an" if name[0].lower() in "aeiou" else "a"} {name} [default: {str(default)}]')
#     var = var or default
#     print(f'Using "{var}" as {name}')
#     return var

library(glue)

get_variable_from_link_or_input <- function(variable, name = 'accession', default = NA) {
    # Get a variable value, either from an ENV VAR that would have been set by the shiny_proxy_jlab_query_parms extension, or through direct user input.
    var <- Sys.getenv(variable, unset = NA)
    if (!is.na(var)) {
        print(glue('Using {name} = {var} from the link you followed.'))
    } else {
        determiner <- ifelse(grepl(tolower(substr(name, 0, 1)), 'aeiou'), 'an', 'a')
        var <- readline(prompt = glue("Type {determiner} {name} [default: {default}]"))
    }
    var <- ifelse(is.na(var) || var == '', default, var)
    print(glue('Using "{var}" as {name}'))
    var
}

