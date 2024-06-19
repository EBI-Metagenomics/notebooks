library(glue)

get_variable_from_link_or_input <- function(variable, name = 'accession', default = NA) {
    # Get a variable value, either from an ENV VAR that would have been set by the jlab_query_params extension, or through direct user input.
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

