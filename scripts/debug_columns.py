#Script pour récupérer les noms des colonnes techniques de l'API. 
import requests
import pandas as pd

url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/evenements-publics-openagenda/records?limit=1"

r = requests.get(url)
data = r.json()["results"]

df = pd.DataFrame(data)

print(df.columns.tolist())