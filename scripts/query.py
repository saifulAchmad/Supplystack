import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from tabulate import tabulate  # Tambahkan import ini
from dotenv import load_dotenv
import os

load_dotenv()
# 
# Azure Search credentials and endpoint
service_name = "content-search"
api_key = str(os.getenv('search_api_key'))
index_name = "suppliers"
endpoint = f"https://{service_name}.search.windows.net"

# Connect to Azure Search
credential = AzureKeyCredential(api_key)
search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

def search_umkm(search_text, provinsi=None, kota=None, kecamatan=None):
    # Build filter string
    filters = []
    if provinsi:
        filters.append(f"provinsi eq '{provinsi}'")
    if kota:
        filters.append(f"kota eq '{kota}'")
    if kecamatan:
        filters.append(f"kecamatan eq '{kecamatan}'")
    
    filter_str = " and ".join(filters)
    
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

# Example usage
search_text = "makanan"  # Search term
provinsi = "Jawa Tengah"  # Filter by Provinsi
kota = "Surakarta"  # Filter by Kota
kecamatan = "Laweyan"  # Filter by Kecamatan

# Perform search and get results in a DataFrame
df_results = search_umkm(search_text, provinsi, kota, kecamatan)

# Display results using tabulate
print("\nMenampilkan seluruh DataFrame menggunakan tabulate:")
print(tabulate(df_results, headers='keys', tablefmt='psql', showindex=False))

# Jika Anda masih ingin menampilkan menggunakan to_string() juga
print("\nMenampilkan seluruh DataFrame menggunakan to_string():")
print(df_results.to_string())