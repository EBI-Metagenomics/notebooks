import requests
import pandas as pd
import numpy as np
import sys
import time
from typing import Optional, Tuple, Union

def format_time(segundos: Union[int,float]) -> str:
    dias = segundos // 86400
    horas = (segundos % 86400) // 3600
    minutos = ((segundos % 86400) % 3600) // 60
    segundos = ((segundos % 86400) % 3600) % 60

    if dias > 1:
        return "> 1 day"
    elif dias == 1:
        return f"{dias} day"
    elif horas > 0:
        return f"{horas}h {minutos}m {segundos}s"
    elif minutos > 0:
        return f"{minutos}m {segundos}s"
    else:
        return f"{segundos}s"


def get_taxonomy_abundances_table(accession: str,vr: float) -> Tuple[Optional[pd.DataFrame],Optional[float]]:
  link = ""
  for d in requests.get("https://www.ebi.ac.uk/metagenomics/api/v1/studies/"+accession+"/downloads").json()["data"]:
    version = float(d["relationships"]["pipeline"]["data"]["id"])
    if version == vr and "Taxonomic assignments" in d["attributes"]["description"]["label"] :
      link = d["links"]["self"]
      print("Version ",version)
      break
  if link == "":
    print("Sorry, this project does not contain 16S data in the MGnify "+str(vr)+" pipeline.")
    return None,None
  else:
    print(link)
    try:
      df = pd.read_csv(link,sep="\t").set_index("#SampleID").T
    except:
      print("Sorry, we were unable to download this data.")
      return None,None
    time = max(1,int(len(df)/250))*4 # each request can get up to 250 samples and takes on average 4s to complete
    print("The estimated duration to obtain metadata is ",format_time(time))

    return df,float(version)

def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False

def requester(url: str,msg: str) -> Optional[dict]:
  max_try=10
  n_try = 0
  sleep_time = 3
  while n_try<max_try:
    try:
      response = requests.get(url).json()
      break
    except:
      print("Fail to request "+msg+"... Trying again in "+str(sleep_time)+"s")
      n_try+=1
      if n_try==max_try:
        sys.exit("Impossible to retrieve the "+msg+". Please check your connection.")
      time.sleep(sleep_time)
  return response

def get_all_runs(accession: str) -> dict:
  url = "https://www.ebi.ac.uk/metagenomics/api/v1/runs?study_accession="+accession+"&page_size=250"
  runs = {}
  while True:
    response = requester(url,"runs")
    for run in response["data"]:
      sampleId = run["relationships"]["sample"]["data"]["id"]
      runId = run["id"]
      if sampleId in runs.keys():
        runs[sampleId].append(runId)
      else:
        runs[sampleId] = [runId]
    # Get next set of runs
    if response["links"]["next"] == None:
      break
    else:
      url = response["links"]["next"]
  return runs

def get_all_samples(accession: str) -> dict[str: list[dict[str:float]]]:
  url = "https://www.ebi.ac.uk/metagenomics/api/v1/samples?study_accession="+accession+"&page_size=250"

  samples = {}
  while True:# Create a getter for connection errors

    response = requester(url,"samples")

    for meta in response["data"]:
      # Get all the attributes with float values
      samples[meta["id"]] = [m for m in meta["attributes"]["sample-metadata"] if is_float(m["value"])]

    if response["links"]["next"] == None:
      break
    else:
      url = response["links"]["next"]
  return samples


def get_metadata(accession: str ,dataIndx: list) -> pd.DataFrame:
  samples = get_all_samples(accession)
  runs = get_all_runs(accession)

  metaData = {}
  # For each sample, check if the sample id was used. If not, try to find the run_id used
  for sampleId in samples.keys():
    if sampleId in dataIndx:
      metaData[sampleId] = samples[sampleId]
    else:
      if sampleId in runs.keys():
        validRunId = [id for id in runs[sampleId] if id in dataIndx] # should be only one run with the valid id...
        if validRunId != []:
          metaData[validRunId[0]] = samples[sampleId] # But I do not trust the system, so get the first one always, no matter if there are more

  #Getting all the possible columns
  keys = set()
  for meta in metaData.values():
    for v in meta:
      keys.add(v["key"])

  #Creating dataframe and replacing missing columns by nan
  df = {c:[] for c in keys}
  df["index"] = []
  for sample in metaData:
    df["index"].append(sample)
    for c in keys:
      if c in [k["key"] for k in metaData[sample]]:# Check if column exists in this sample
        df[c].append([d["value"] for d in metaData[sample] if d["key"] == c][0])
      else:
        df[c].append(np.nan)

  # Casting the result as a pandas dataframe
  df = pd.DataFrame(df)
  df = df.set_index("index")
  df = df.apply(pd.to_numeric, errors='ignore')
  return df

def get_data_and_metadata_from_project(accession: str,version : float = 5.0) -> tuple[Optional[pd.DataFrame],Optional[pd.DataFrame],Optional[float]]:
  data, v = get_taxonomy_abundances_table(accession,version)
  if type(data) != type(None):
    dataIDList = list(data.index)# Get the first 3 letters of a sample id from the data

    meta = get_metadata(accession,dataIDList)
    if type(meta) != type(None):
      totsamples = len([i for i in meta.index if i in data.index]) # Check total of usable samples

      if totsamples == 0:
        print("Sorry, no valid metadata was found for this project.")
        return None,None,None #Trocar de volta depois
      if totsamples<25:
        print("\nWARNING! The number of samples in this project is too low. May lead to spurious results.\n")

      print("This project contains a total of ",totsamples," samples.\n")
      return data,meta,v
    else:
      return None,None,None
  else:
    if version != 4.1:
      print("Trying to rescue data for version 4.1...")
      return get_data_and_metadata_from_project(accession = accession,version = 4.1)
    return None,None,None