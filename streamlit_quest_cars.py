import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
st.set_page_config(layout="wide")

df = pd.read_csv('https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv')
df2 = df.iloc[:,:-1]

# A METTRE EN PLACE, SCRIPT DIFFERENT EN FONCTION DU MODE DE LECTURE DU USER
# Vérifie le thème actuel de Streamlit
#theme = st.get_theme()

# Vérifie si le thème est un thème sombre
#is_dark = theme["theme"] == "dark"

# Si le thème est sombre
#if is_dark:
    # Exécutez ce code pour le mode sombre
#else:
    # Exécutez ce code pour le mode clair


## TITRE
st.container()

with st.container():
    st.markdown(f"<h1 style='text-align: center;'>Dataset cars Analysis via Streamlit</h1>", unsafe_allow_html=True)
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
    st.markdown(f"<h2 style='text-align: center; color: #3ae098;'>Heatmap : Correlation map</h2>", unsafe_allow_html=True)
    st.write('mpg, ie miles per gallon')
    st.write('cubic inches, ie a measurement of the size of the chamber where fuel is burned in a car engine')
    st.write('hp, ie housepower')
    st.write('weightlbs, ie weight in pounds')
    st.write('We can see a strong positive correlation between cylinders and cubic inches, house power and weightlbs')
    st.write('Also we observe a negative correlation between mpg and the 4 criteria above')

## GRAPHIQUE EN BARRE AVEC SELECTION CONTINENT [#ET YEAR]

select_container, graph_container = st.columns([2, 3])

with select_container:
    
    st.markdown(f"<h2 style='text-align: center; color: #cc3d55;'>Number of cars by continent and years</h2>", unsafe_allow_html=True)
    st.write("Please select the continent you want to compare")
    df['continent'] = df['continent'].str.replace('.', '')
    continents = df['continent'].unique()
    selected_continent = st.multiselect('Choose below',  continents)

    
    if selected_continent:
        df = df[df['continent'].isin(selected_continent)]
   
    
#    st.write("Please select the period of time you want to analyse")
#    years = st.slider('Select below', min_value=df['year'].min(), max_value=df['year'].max(), value=(df['year'].min(), df['year'].max()))
#    
#   if years:
#        df = df.loc[(df['year'] >= years[0]) & (df['year'] <= years[1])]


with graph_container:
    colors = {'France': 'red','US': '#26f0c7', 'Europe' :' #c4f026', 'Japan': '#14e8f7'}
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

## GRAPHIQUE EN BULLE HOUSE POWER x WEIGHT BY SIZE OF CYLINDER
main_container2 = st.container()
graph_container2, col2, text_container2 = main_container2.columns([2, 1, 2])

with graph_container2:
    colors = {'France': 'red','US': '#26f0c7', 'Europe' :' #c4f026', 'Japan': '#14e8f7'}
    fig, ax = plt.subplots(figsize=(5, 3))
    fig = px.scatter(df, x='hp', y='weightlbs', color='continent', labels={'hp': 'house power', 'weightlbs': 'weight of the vehicule'})
    fig.update_layout({'plot_bgcolor': '#0E1117', 'paper_bgcolor': '#0E1117'})
    fig.update_traces(marker=dict(size=10, line=dict(width=2, color='white')))
        
    st.plotly_chart(fig)

with col2:
    st.write('')

with text_container2:
    st.markdown(f"<h2 style='text-align: center; color: #faefa0;'>Cars distribution by house power & weight</h2>", unsafe_allow_html=True)
    st.write('As we can see on the scatterplot, if you like vehicle with the highest house power, you need to focus on US cars.')
    st.write('There is a strong relation between house power and weight of the car')
    st.write('On the other side, French and Japanese cars are less powerful and lighter than US car, regarding cars between 1971 and 1983.')


# cd C:\Users\steph\Desktop\Test_streamlit\Quest_cars
# streamlit run "C:\Users\steph\Desktop\Test_streamlit\Quest_cars\streamlit_quest_cars.py"
