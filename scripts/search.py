import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from tabulate import tabulate  # Tambahkan import ini
from dotenv import load_dotenv
import os

load_dotenv()

# Azure Search credentials and endpoint
service_name = "content-search"
api_key = str(os.getenv('search_api_key'))
index_name = "suppliers"
endpoint = f"https://{service_name}.search.windows.net"

# Connect to Azure Search
credential = AzureKeyCredential(api_key)
search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

# Function to query Azure Search
def get_supplier(search_text, provinsi=[], kota=[], kecamatan=[]):
    # Build filter string
    filters = []
    if provinsi:
        f = []
        for prov in provinsi:
            f.append(f"provinsi eq '{prov}'")
        filters.append(f'({" or ".join(f)})')

    if kota:
        f = []
        for k in kota:
            f.append(f"kota eq '{k}'")
        filters.append(f'({" or ".join(f)})')

    if kecamatan:
        f = []
        for k in kecamatan:
            f.append(f"kecamatan eq '{k}'")
        filters.append(f'({" or ".join(f)})')
    
    filter_str = " and ".join(filters)
    print(f'filter_str: {filter_str}')
    openai_api_key = str(os.getenv('open_api_key'))

    # Perform search
    results = search_client.search(search_text=search_text, filter=filter_str)
    
    # Extract results into a list of dictionaries
    documents = []
    for result in results:
        doc = {
            'id': result['id'],
            'bidang': result['bidang'],
            'supplier': result['supplier'],
            'deskripsi': result['deskripsi'],
            'barang': result['barang'],
            'provinsi': result['provinsi'],
            'kota': result['kota'],
            'kecamatan': result['kecamatan']
        }
        documents.append(doc)
    
    # Convert to DataFrame
    df = pd.DataFrame(documents)
    
    return df

