import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

st.title("Street Crime Analysis in London")

# Conectar com Snowflake usando o secrets.toml
def get_snowflake_connection():
    return snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        role=st.secrets["snowflake"]["role"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

@st.cache_data(ttl=600)
def load_street_data():
    conn = get_snowflake_connection()
    query = """SELECT * FROM crimes_in_london_db.crimes_in_london_schema."table_street";"""
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Carregar os dados
street_data = load_street_data()
street_data = street_data.drop(columns=["CRIME_ID"])
street_data = street_data.drop(columns=["CONTEXT"])

# Filtros na barra lateral
crime_types = st.sidebar.multiselect("Select Crime Type", options=street_data["CRIME_TYPE"].unique())
regions = st.sidebar.multiselect("Select Region", options=street_data["REPORTED_BY"].unique())
months = st.sidebar.multiselect("Select Month", options=street_data["MONTH"].unique())

# Aplicar os filtros
if crime_types:
    street_data = street_data[street_data["CRIME_TYPE"].isin(crime_types)]
if regions:
    street_data = street_data[street_data["REPORTED_BY"].isin(regions)]
if months:
    street_data = street_data[street_data["MONTH"].isin(months)]

# Exibir a tabela paginada
st.dataframe(street_data, height=300)

# Verificar se as colunas 'LATITUDE' e 'LONGITUDE' existem
if 'LATITUDE' in street_data.columns and 'LONGITUDE' in street_data.columns:
    # Gráfico
    fig = px.scatter_mapbox(street_data, lat="LATITUDE", lon="LONGITUDE", color="CRIME_TYPE", zoom=10)
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)
else:
    st.warning("As colunas 'LATITUDE' e 'LONGITUDE' não estão disponíveis no conjunto de dados.")
