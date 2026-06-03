# Retrieve name and URL for a specific pathway in the KEGG database 
get_pathway_info <- function(pathway) {
  pathway <- paste("map", pathway, sep = "")
  pathway_name <- keggList(pathway)[[1]]
  pathway_url <- paste("https://www.kegg.jp/pathway/", pathway, sep = "")
  return(list(pathway_name = pathway_name, pathway_url = pathway_url))
}


# Function to prompt users for pathway selection and return custom pathway IDs
PathwaysSelection <- function() {
    display_markdown("#### Pathways Selection :\n\n
- For the most general & most complete pathways, input 'G'\n\n
- Press Enter to generate the most complete pathways\n\n
- To add custom pathways, input pathway numbers (ex: 00053,01220)")
    
  flush.console()
  CUSTOM_PATHWAY_IDS <- get_variable_from_link_or_input('CUSTOM_PATHWAY_IDS', name = 'Pathways Accession', default = '')
  
  if (CUSTOM_PATHWAY_IDS == "") {
    CUSTOM_PATHWAY_IDS <- list()
  } else if (CUSTOM_PATHWAY_IDS == "G") {
    CUSTOM_PATHWAY_IDS <- list("00010", "00020", "00030", "00061", "01232","00240", "00190")
  } else {
    CUSTOM_PATHWAY_IDS <- strsplit(CUSTOM_PATHWAY_IDS, ",")[[1]]
  }
  
  message(if (length(CUSTOM_PATHWAY_IDS) > 0) {
    paste("\nUsing", CUSTOM_PATHWAY_IDS, " - ", sapply(CUSTOM_PATHWAY_IDS, function(id) paste(get_pathway_info(id)[1]," : ",get_pathway_info(id)[2])), "as a Custom Pathway")
  } else {
    "\nUsing NONE as a Custom Pathway"
  })
    return(CUSTOM_PATHWAY_IDS)
}

          
# Clearing the current working directory and displaying generated figures from `pathway_plots/` directory
generatePathwayPlots <- function() {
# Clearing the current working directory
  if (!dir.exists("pathway_plots")) {
    dir.create("pathway_plots")
  }

  file.copy(from = list.files(pattern = "./*pathview.png"), to = "./pathway_plots/", overwrite = TRUE)

  png_files <- list.files(path = ".", pattern = "*.png")
  xml_files <- list.files(path = ".", pattern = "*.xml")
  files <- c(png_files, xml_files)
  output <- capture.output({
    unlink(files)
  })
  
# Accessing the png files and displaying it
  images <- list.files("pathway_plots", full.names = TRUE)

  for (pathway in images) {
    display_markdown(get_pathway_info(gsub("[^0-9]", "", basename(pathway)))$pathway_name)
    display_png(file = pathway)
  }
}