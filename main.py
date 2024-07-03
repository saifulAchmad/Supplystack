import streamlit as st
import pandas as pd

from scripts.search import get_supplier

from dotenv import load_dotenv
import os

load_dotenv()



df_lokasi = pd.read_csv("umkm.csv")
df_lokasi = df_lokasi[['provinsi', 'kota' , 'kecamatan']].drop_duplicates()

columns_to_remove = [col for col in df_lokasi.columns if col == '']
if columns_to_remove:
    df_lokasi = df_lokasi.drop(columns=columns_to_remove)
st.title("Cari Supplier")

st.sidebar.title("Pilih Lokasi")

with st.sidebar:
    selected_province = st.multiselect("Pilih Provinsi :", df_lokasi['provinsi'].unique())
    
    if selected_province:
        filtered_cities = df_lokasi[df_lokasi['provinsi'].isin(selected_province)]['kota'].unique()
    else:
        filtered_cities = df_lokasi['kota'].unique()

    selected_cities = st.multiselect("Pilih Kota :", filtered_cities, disabled=len(selected_province) > 1)

    if selected_cities:
        filtered_districts = df_lokasi[df_lokasi['kota'].isin(selected_cities)]['kecamatan'].unique()
    else:
        filtered_districts = df_lokasi['kecamatan'].unique()

    selected_districts = st.multiselect("Pilih Kecamatan :", filtered_districts, disabled=len(selected_cities) > 1)

    
    # if selected_districts:
    #     filtered_industries = df[df['kecamatan'].isin(selected_districts)]['bidang'].unique()
    # else:
    #     filtered_industries = df['bidang'].unique()

    # selected_industries = st.multiselect("Pilih bidang :", filtered_industries)


print((selected_province, selected_cities, selected_districts))

filtered_df = df_lokasi.copy()

if selected_province:
    filtered_df = filtered_df[filtered_df['provinsi'].isin(selected_province)]

if selected_cities:
    filtered_df = filtered_df[filtered_df['kota'].isin(selected_cities)]

if selected_districts:
    filtered_df = filtered_df[filtered_df['kecamatan'].isin(selected_districts)]


# search_description = st.text_input('Deskripsi')
# search_by_description = ''

text_services = st.text_input('Barang atau Jasa')
search_services_ = st.button('Search', type='primary')
if search_services_:
    df_search = get_supplier(text_services, provinsi=selected_province, kota=selected_cities, kecamatan=selected_districts)
    st.session_state['df_search'] = df_search

df_search = st.session_state.get('df_search', None)
if df_search is not None:
    st.dataframe(df_search)

# if selected_industries:
#     filtered_df = filtered_df[filtered_df['bidang'].isin(selected_industries)]

# st.dataframe(filtered_df)


# # Example usage
# search_text = "makanan"  # Search term
# provinsi = "Jawa Tengah"  # Filter by Provinsi
# kota = "Surakarta"  # Filter by Kota
# kecamatan = "Laweyan"  # Filter by Kecamatan

# # Perform search and get results in a DataFrame
# df_results = search_umkm(search_text, provinsi, kota, kecamatan)

# # Display results using tabulate
# print("\nMenampilkan seluruh DataFrame menggunakan tabulate:")
# print(tabulate(df_results, headers='keys', tablefmt='psql', showindex=False))

# # Jika Anda masih ingin menampilkan menggunakan to_string() juga
# print("\nMenampilkan seluruh DataFrame menggunakan to_string():")
# print(df_results.to_string())