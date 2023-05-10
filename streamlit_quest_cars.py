import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
st.set_page_config(layout="wide")

df = pd.read_csv('https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv')
df2 = df.iloc[:,:-1]


## TITRE
st.container()

with st.container():
    st.markdown(f"<h1 style='text-align: center;'>Analyse dataset cars via Streamlit</h1>", unsafe_allow_html=True)
    st.write("")

## GRAPHIQUE MAP DE CORRELATION AVEC TEXTE A COTE
main_container = st.container()

graph_container, text_container = main_container.columns([3, 2])

with graph_container:
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.heatmap(df2.corr(), cmap=sns.color_palette("viridis"), center = 0, annot= True, annot_kws={"fontsize":6}, fmt='.2f', ax=ax)
    fig.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    ax.tick_params(axis='x', colors='white', rotation=45, labelsize=6)
    ax.tick_params(axis='y', colors='white', labelsize=6)
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(color='white', labelcolor='white', labelsize=6)

    st.pyplot(fig)

with text_container:
    st.markdown(f"<h2 style='text-align: center; color: #3ae098;'>Map de corrélation</h2>", unsafe_allow_html=True)
    st.write('mpg = miles per gallon, soit proche de la consommation du litre au 100kms')
    st.write('cubicinches soit pouces cubes')
    st.write('hp soit la puissance du véhicule')

## GRAPHIQUE EN BARRE AVEC SELECTION CONTINENT ET YEAR

select_container, graph_container = st.columns([2, 3])

with select_container:
    
    st.markdown(f"<h2 style='text-align: center; color: #cc3d55;'>Number of cars by continent and years</h2>", unsafe_allow_html=True)
    df['year'] = pd.to_datetime(df['year'], format = '%Y')
    df['year'] = df['year'].dt.year

    st.write("Please select the continent you want to compare")
    continents = df['continent'].unique()
    selected_continent = st.multiselect('Choose below',  continents)

    if selected_continent:
        df = df[df['continent'].isin(selected_continent)]

    st.write("Please select the period of time you want to analyse")
    year_range = st.slider('Select below', min_value=df['year'].min(), max_value=df['year'].max(), value=(df['year'].min(), df['year'].max()))

    #df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

with graph_container:
    colors = {'France': 'red','US.': '#26f0c7', 'Europe.' :' #c4f026', 'Japan.': '#14e8f7'}
    fig, ax = plt.subplots(figsize=(7, 5))
    fig = px.histogram(df, x='year', color='continent', barmode='group', color_discrete_map=colors)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(
        l=50,
        r=50,
        t=50,
        b=50
    ),yaxis_title='Nombre de voitures', xaxis_title='',
                  bargap=0.2)
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    fig.update_xaxes(tickvals=df['year'].unique(),
                 ticktext=df['year'].unique(),
                 dtick=1)

    st.plotly_chart(fig)

