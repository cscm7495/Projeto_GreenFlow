import streamlit as st
import pandas as pd
import altair as alt


# Import and read cleaned file
file_path = 'data/dados_sensores_5000_limpos.parquet'
df = pd.read_parquet(file_path)

# Set app layout
st.set_page_config(layout="wide")

# Set app logo & title
st.image("assets/logo.png", width=150)
st.title("Sensores Ambientais")
st.write("Gastos de energia, CO2 e Água")


# Analyse data and build visuals
# Consumption per sector
st.header('Consumos Por Setor')
st.write ('Média de consumos totais e consumos totais e por setor')

# Energy Consumption

# Average energy consumption - total and per sector
st.subheader('Energia')
st.write ("Média de consumo de energia/kwh por empresa; Média por empresa por setor; Consumo Total de Energia/kwh por Setor")
col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
with col1:
    avg_energy_kwh = round(df['energia_kwh'].mean(), 2)
    st.metric(
        label="Média por empresa",
        value=avg_energy_kwh)

with col2:
    avg_energy_kwh_per_setor = df.groupby('setor')['energia_kwh'].mean().round(2)
    setor_options = df['setor'].unique()
    selected_setor = st.selectbox('Selecione um Setor', setor_options,  key='avg_energia_kwh')

with col3:
    if selected_setor:
        st.metric(
        label=f'Média por empresa no setor de {selected_setor}',
        value=avg_energy_kwh_per_setor[selected_setor])

# Energy consumption per setor
with col4:
    energy_per_sector = df.groupby('setor')['energia_kwh'].sum().reset_index()
    st.bar_chart(
        data=energy_per_sector,
        x="setor",
        y="energia_kwh",
        color="#99d98c",
        horizontal=True)

# Water consumption
st.subheader('Água')
st.write ("Média de consumo de agua/m3 por empresa; Média por empresa por setor; Consumo Total de agua/m3 por Setor")
col5, col6, col7, col8 = st.columns([1, 1, 1, 3])


# Average water consumption - total and per sector
with col5:
    avg_agua_m3 = round(df['agua_m3'].mean(), 2)
    st.metric(
        label="Média Água/m3",
        value=avg_agua_m3)

with col6:
    avg_agua_m3_per_setor = df.groupby('setor')['agua_m3'].mean().round(2)
    setor_options = df['setor'].unique()
    selected_setor = st.selectbox('Selecione um Setor', setor_options, key='avg_agua_m3')

with col7:
    if selected_setor:
        st.metric(
        label=f'Média Água/m3 no setor de {selected_setor}',
        value=avg_agua_m3_per_setor[selected_setor])

# Water consumption per setor
water_per_sector = df.groupby('setor')['agua_m3'].sum().reset_index()
with col8:
   st.bar_chart(
       data=water_per_sector,
       x="setor",
       y="agua_m3",
       color="#168aad",
       horizontal=True)

# CO2 Emissions
st.subheader('Emissões CO2')
st.write ("Média de emissões CO2 por empresa; Média por empresa por setor; Emissão Total de CO2 por Setor")
col9, col10, col11, col12 = st.columns([1, 1, 1, 3])

# Average co2 emissions - total and per sector
with col9:
    avg_co2 = round(df['co2_emissoes'].mean(), 2)
    st.metric(
        label="Média Emissões CO2",
        value=avg_co2)

with col10:
    avg_co2_per_setor = df.groupby('setor')['co2_emissoes'].mean().round(2)
    setor_options = df['setor'].unique()
    selected_setor = st.selectbox('Selecione um Setor', setor_options, key='avg_co2_emissoes')

with col11:
    if selected_setor:
        st.metric(
        label=f'Média Emissões C02 no setor de {selected_setor}',
        value=avg_co2_per_setor[selected_setor])


# CO2 emissions per setor
co2_per_sector = df.groupby('setor')['co2_emissoes'].sum().reset_index()
with col12:
  st.bar_chart(
      data=co2_per_sector,
      x="setor",
      y="co2_emissoes",
      color="#d9ed92",
      horizontal=True)

# Consumption per company, based on sector
st.header('Consumos Por Empresa e Setor')
st.write ('Consumos por empresa, com base no setor a que pertencem')

# Create a dictionary mapping each setor to its corresponding empresas
setor_to_empresas = df.groupby('setor')['empresa'].apply(list).to_dict()

# Energy data per company
st.subheader('Energia')

# Finding the company with the least and most energy consumption overall
least_energy_kwh = df['energia_kwh'].min()
least_energy_company_setor = df.loc[df['energia_kwh'].idxmin()]
most_energy_kwh = df['energia_kwh'].max()
most_energy_company_setor = df.loc[df['energia_kwh'].idxmax()]

col13, col14, col15= st.columns([3,6,6])
with col14:
    st.metric(
        label=f'Empresa com menor gasto energético',
        value=least_energy_kwh)
    st.write(f"Empresa: {least_energy_company_setor['empresa']}")
    st.write(f"Setor: {least_energy_company_setor['setor']}")

with col15:
    st.metric(
        label=f'Empresa com maior gasto energético',
        value=most_energy_kwh)
    st.write(f"Empresa: {most_energy_company_setor['empresa']}")
    st.write(f"Setor: {most_energy_company_setor['setor']}")

# Create filter selection for companies to analyse their energy consumption
# Filter by sector
selected_setor = st.selectbox("Selecione um Setor", options=df['setor'].unique(), key='setor_energia_kwh')
# Get companies in the selected sector
empresas_energia = setor_to_empresas.get(selected_setor, [])
# Sort companies in the selected sector by energia_kwh in descending order
sorted_empresas = df[df['setor'] == selected_setor].sort_values(by='energia_kwh')['empresa'].tolist()[:5]
# Filter by empresa
selected_empresas = st.multiselect("Select Empresas", options=empresas_energia, default=sorted_empresas, key='empresa_energia_kwh')
# Filter data based on selections
filtered_df = df[(df['empresa'].isin(selected_empresas)) & (df['setor'] == selected_setor)]

# Bar chart
st.bar_chart(
    data=filtered_df.set_index('empresa')[['energia_kwh']],
    color="#99d98c")

# Water data
st.subheader('Água')

# Finding the company with the least and most water consumption overall
least_water_m3 = df['agua_m3'].min()
least_water_company_setor = df.loc[df['agua_m3'].idxmin()]
most_water_m3 = df['agua_m3'].max()
most_water_company_setor = df.loc[df['agua_m3'].idxmax()]

col16, col17, col18= st.columns([3,6,6])
with col17:
    st.metric(
        label=f'Empresa com menor gasto água/m3',
        value=least_water_m3)
    st.write(f"Empresa: {least_water_company_setor['empresa']}")
    st.write(f"Setor: {least_water_company_setor['setor']}")

with col18:
    st.metric(
        label=f'Empresa com maior gasto água/m3',
        value=most_water_m3)
    st.write(f"Empresa: {most_water_company_setor['empresa']}")
    st.write(f"Setor: {most_water_company_setor['setor']}")


# Create filter selection for companies to analyse their water consumption
# Filter by sector
selected_setor = st.selectbox("Selecione um Setor", options=df['setor'].unique(), key='setor_agua_m3')
# Get companies in the selected sector
empresas_energia = setor_to_empresas.get(selected_setor, [])
# Sort companies in the selected sector by agua_m3 in descending order
sorted_empresas = df[df['setor'] == selected_setor].sort_values(by='agua_m3')['empresa'].tolist()[:5]
# Filter by empresa
selected_empresas = st.multiselect("Select Empresas", options=empresas_energia, default=sorted_empresas, key='empresa_agua_m3')
# Filter data based on selections
filtered_df = df[(df['empresa'].isin(selected_empresas)) & (df['setor'] == selected_setor)]

# Bar chart
st.bar_chart(
    data=filtered_df.set_index('empresa')[['agua_m3']],
    color="#168aad")

# CO2 Data
st.subheader('Emissões CO2')

# Finding the company with the least and most co2 emissions overall
least_co2 = df['co2_emissoes'].min()
least_co2_company_setor = df.loc[df['co2_emissoes'].idxmin()]
most_co2 = df['co2_emissoes'].max()
most_co2_company_setor = df.loc[df['co2_emissoes'].idxmax()]

col19, col20, col21= st.columns([3,6,6])
with col20:
    st.metric(
        label=f'Empresa com menores emissões CO2',
        value=least_co2)
    st.write(f"Empresa: {least_co2_company_setor['empresa']}")
    st.write(f"Setor: {least_co2_company_setor['setor']}")

with col21:
    st.metric(
        label=f'Empresa com maiores emissões CO2',
        value=most_co2)
    st.write(f"Empresa: {most_co2_company_setor['empresa']}")
    st.write(f"Setor: {most_co2_company_setor['setor']}")


# Filter by sector
selected_setor = st.selectbox("Selecione um Setor", options=df['setor'].unique(), key='setor_co2')
# Get companies in the selected sector
empresas_energia = setor_to_empresas.get(selected_setor, [])
# Sort companies in the selected sector by co2_emissoes in descending order
sorted_empresas = df[df['setor'] == selected_setor].sort_values(by='co2_emissoes')['empresa'].tolist()[:5]
# Filter by empresa
selected_empresas = st.multiselect("Select Empresas", options=empresas_energia, default=sorted_empresas, key='empresa_co2')
# Filter data based on selections
filtered_df = df[(df['empresa'].isin(selected_empresas)) & (df['setor'] == selected_setor)]

# Bar chart
st.bar_chart(
    data=filtered_df.set_index('empresa')[['co2_emissoes']],
    color="#d9ed92")

# Histograms
st.header('Contagem de empresas por escalão de consumo')
st.write ('Contagem de empresas por escalão de consumo no total e por setor')

st.subheader('Energia')

def histogram_energia_setor(df, selected_setor):
    colors = {
        'Educação': '#74c69d',
        'Saúde': '#52b788',
        'Indústria': '#40916c',
        'Alimentação': '#2d6a4f',
        'Varejo': '#1b4332',
        'Serviços': '#081c15'
    }

    chart = alt.Chart(df[df['setor'] == selected_setor]).mark_bar().encode(
        alt.X("energia_kwh:Q", bin=True),
        y='count()',
        color=alt.value(colors.get(selected_setor, '#74c69d'))
    )
    return chart

def histogram_energia_total(df):
    chart = alt.Chart(df).mark_bar(color='#99d98c').encode(
        alt.X("energia_kwh:Q", bin=True),
        y='count()',
    )
    return chart

col22, col23 = st.columns([4,4])
with col22:
    st.write("")  # Add a blank space
    st.write("")  # Add another blank space
    st.write("")  # Add a blank space
    st.write("")  # Add another blank space
    st.write("")  # Add another blank space
    chart = histogram_energia_total(df)
    st.altair_chart(chart, use_container_width=True)

with col23:
    selected_setor = st.selectbox("Selecione um Setor:", df['setor'].unique(), key="histogram_energia")

    chart = histogram_energia_setor(df, selected_setor)
    st.altair_chart(chart, use_container_width=True)


st.subheader('Água')

def histogram_agua_setor(df, selected_setor):
    colors = {
        'Educação': '#468faf',
        'Saúde': '#2c7da0',
        'Indústria': '#2a6f97',
        'Alimentação': '#014f86',
        'Varejo': '#014f862',
        'Serviços': '#013a63'
    }

    chart = alt.Chart(df[df['setor'] == selected_setor]).mark_bar().encode(
        alt.X("agua_m3:Q", bin=True),
        y='count()',
        color=alt.value(colors.get(selected_setor, '#468faf'))
    )
    return chart

def histogram_agua_total(df):
    chart = alt.Chart(df).mark_bar(color='#168aad').encode(
        alt.X("agua_m3:Q", bin=True),
        y='count()',
    )
    return chart

col24, col25 = st.columns([4,4])
with col24:
    st.write("")  # Add a blank space
    st.write("")  # Add another blank space
    st.write("")  # Add a blank space
    st.write("")  # Add another blank space
    st.write("")  # Add another blank space
    chart = histogram_agua_total(df)
    st.altair_chart(chart, use_container_width=True)

with col25:
    selected_setor = st.selectbox("Selecione um Setor:", df['setor'].unique(), key="histogram_agua")

    chart = histogram_agua_setor(df, selected_setor)
    st.altair_chart(chart, use_container_width=True)


st.subheader('Emissões CO2')

def histogram_co2_setor(df, selected_setor):
    colors = {
        'Educação': '#fad643',
        'Saúde': '#edc531',
        'Indústria': '#dbb42c',
        'Alimentação': '#c9a227',
        'Varejo': '#b69121',
        'Serviços': '#a47e1b'
    }

    chart = alt.Chart(df[df['setor'] == selected_setor]).mark_bar().encode(
        alt.X("co2_emissoes:Q", bin=True),
        y='count()',
        color=alt.value(colors.get(selected_setor, '#fad643'))
    )
    return chart

def histogram_co2_total(df):
    chart = alt.Chart(df).mark_bar(color='#d9ed92').encode(
        alt.X("co2_emissoes:Q", bin=True),
        y='count()',
    )
    return chart

col26, col27 = st.columns([4,4])
with col26:
    st.write("")  # Add a blank space
    st.write("")  # Add another blank space
    st.write("")  # Add a blank space
    st.write("")  # Add another blank space
    st.write("")  # Add another blank space
    chart = histogram_co2_total(df)
    st.altair_chart(chart, use_container_width=True)

with col27:
    selected_setor = st.selectbox("Selecione um Setor:", df['setor'].unique(), key="histogram_co2")

    chart = histogram_co2_setor(df, selected_setor)
    st.altair_chart(chart, use_container_width=True)