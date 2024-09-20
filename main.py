import streamlit as st

st.title("Crimes in London Analysis")
st.write("""
Welcome to the London Crimes Dashboard. Use the sidebar to navigate through different pages and filter the data.
""")

# Centralizar a bandeira
st.image("london_flag.jpg", use_column_width=True)

# Texto com o hyperlink
st.markdown("""
The data has been extracted from [https://data.police.uk/about](https://data.police.uk/about), so they are real data.
""")
