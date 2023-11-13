import requests
import math
import pandas as pd
from io import StringIO
from IPython.display import display, Markdown, HTML
import altair as alt
from altair import datum
import graphviz

def get_GO_metadata(accession):
    """
    Retrieve GO metadata for a given study accession using the EBI Metagenomics API.
    """
    try:
        url = f"https://www.ebi.ac.uk/metagenomics/api/v1/studies/{accession}/downloads"
        response = requests.get(url)
        response.raise_for_status()  

        data = response.json()["data"]
        filtered_data = [item for item in data if item['attributes']['description']['label'] in ['GO slim annotation', 'Complete GO annotation']]
        
        if not filtered_data:
            raise Exception("*** No GO annotation Data found for the specified Study accession. ***")
            
        df = pd.json_normalize(filtered_data)[['id', 'attributes.description.label', 'relationships.pipeline.data.id', 'links.self']]
        df.columns = ['Name', 'Label', 'Pipeline', 'Link']
        df['Pipeline'] = df['Pipeline'].astype(float)
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    
def display_GO_metadata(df):
    """
    Display GO metadata for a given study accession using the EBI Metagenomics API.
    """
    x,y = df[df["Label"]=="GO slim annotation"].sort_values("Pipeline",ascending=False), df[df["Label"]=="Complete GO annotation"].sort_values("Pipeline",ascending=False)
    return display(Markdown('**GO Slim annotation Metadata**'), x, Markdown('<br>**Complete GO annotation Metadata**'), y)

def download_GO_data(label,go_metadata):
    try:
        pipeline_version = input(f"For downloading {label} data,\nEnter Pipeline Version (or press Enter for the most recent version): ")
        pipeline_version = float(pipeline_version) if pipeline_version.strip() else max(go_metadata["Pipeline"])
        print(f'\nUsing "{pipeline_version}" as Pipeline Version')
        filtered_data = go_metadata[(go_metadata["Label"] == label) & (go_metadata["Pipeline"] == pipeline_version)]
        if not filtered_data["Link"].empty:
            download_link = filtered_data["Link"].iloc[0]
        else:
            raise Exception(f"{label} data for Pipeline Version - {pipeline_version} not found!!! Try another version.")
        display(Markdown(f"<br>**Dowloading {label} Data**"))
        response = requests.get(download_link)
        response.raise_for_status()   
        df = pd.read_csv(StringIO(response.text), delimiter='\t')
        df["Total Annotations"] = df.iloc[:, 3:].sum(axis=1).astype(int)
        display(HTML('&#10004; Data Loaded Successfully'))
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.RequestException as err:
        print("Request Error:", err)
    return df

def GO_Bar(Category, Title, Color, df):
    df.sort_values(by='Total Annotations', ascending=False, inplace=True)
    base = alt.Chart(df).properties(height=650)
    return base.mark_bar(color=Color).encode(
        alt.Y('description:N').sort('-x').title(None).axis(labelColor="#666"),
        alt.X('Total Annotations:Q').title("Total Annotations").axis(orient="top",titleColor= "#666", labelColor="#666",format="s"),
        tooltip=["GO","description","Total Annotations"]).transform_filter(
    datum.category == Category).properties(title=Title)

def process_subclass(go_term, GO_complete, parent=None,ChartData=None):
    if ChartData is None:
        ChartData = pd.DataFrame(columns=GO_complete.columns)
        ChartData.insert(1, 'Parent', None)
        
    if parent is None:
        parent = 0
        
    filtered_rows = GO_complete[GO_complete["GO"] == go_term].copy()
    filtered_rows["Parent"] = parent
    ChartData = pd.concat([ChartData, filtered_rows])
    
    url = f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{go_term}/children" 
    try:
        children_data = requests.get(url, headers={"Accept": "application/json"}).json()
        children = children_data["results"][0]["children"]
        if children:
            for child in children:
                if child["id"] in GO_complete["GO"].values:
                    print(child["id"], end=" ")
                    ChartData = process_subclass(child["id"], GO_complete, go_term, ChartData)
        
        else:
            print(f"No children found for GO term '{go_term}'")

    except Exception as e:
            pass
    return ChartData.drop_duplicates()

def GO_tree(ChartData,assembly_run="Total Annotations"):
    print("\n\n")
    
    num_nodes = len(ChartData)

    # Define a base size for the graph
    base_size = 10
    scale_factor = math.sqrt(num_nodes)
    
    # Adjust the base size with the scale factor
    graph_size = f'{base_size * scale_factor},{(base_size * scale_factor) / 10}'
    graph = graphviz.Digraph(graph_attr={'size': graph_size, 'center': 'true'})
    graph.attr('node', shape='box', style='filled, rounded', width='1', height='1', color='lightblue')
    graph.attr('edge',color= 'gray', penwidth='4')
    graph.attr(nodesep='0.5')
    graph.attr(ranksep='1.0')
    graph.attr(layout='dot')
    graph.attr(overlap="false")
    # graph.attr(splines="spline")
    
    for index, row in ChartData.iterrows():
        child_id = row['GO']
        parent_id = row['Parent']
        value = row[assembly_run]
        label = row['description']
        node_label = f"{child_id}\n{label}\n\n{assembly_run}: {value}"

        graph.node(child_id.replace('GO:', ''), node_label)

        if parent_id != 0:
            graph.edge(parent_id.replace('GO:', ''), child_id.replace('GO:', ''))
            
    graph.attr(label=f'\n\nDescendant Tree for the Assembly Run : {assembly_run}')
    graph.render()
    return graph

def GO_heatmap(ChartData):
    ChartData = ChartData.copy()
    ChartData.drop("category", axis=1, inplace=True)
    ChartData.drop("Parent", axis=1, inplace=True)
    ChartData.drop("Total Annotations", axis=1, inplace=True)
    ChartData = ChartData.drop_duplicates()
    
    ChartData = pd.melt(ChartData, id_vars=['GO', 'description'], var_name='Assembly Run', value_name='Value')

    color_scale = alt.Scale(domain=[0, 1e3, 1e6])
    chart = alt.Chart(ChartData).mark_rect(stroke='#666', strokeWidth=0.2).encode(
        x=alt.X('Assembly Run:O', title="Assembly Run").axis(orient="top", labelOverlap=True,labelFontSize=8),
        y=alt.Y('GO:O', title=None, sort=alt.Order()).axis(labelFontSize=12),
        color=alt.Color('Value:Q', title="Value", scale=color_scale),
        tooltip=[alt.Tooltip("GO:N", title="GO"), "description:N", alt.Tooltip("Value:Q", title="Value"),
                 "Assembly Run:O"]
    ).properties(
        width=1200,
        height=500,
        title="Heatmap of GO vs. Assembly Runs"
    )
    chart.configure_axis(
        labelFontSize=8,
        titleFontSize=14,
    ).configure_legend(
        # orient="top"
    ).configure_title(
        fontSize=16,
        fontWeight='bold',
    )
    
    return chart