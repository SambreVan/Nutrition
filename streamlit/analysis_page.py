# analysis_page.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_analysis_page():
    st.title("Analyse des Produits Alimentaires")


    data = pd.read_csv("DataPres/sampled_output.csv")

    
    st.write("Colonnes du DataFrame:", data.columns.tolist())

    
    if 'Catégorie' in data.columns:
        data_filtered = data[data['Catégorie'] != 'Produit_Sans_Nom']
    else:
        st.error("La colonne 'Catégorie' est manquante dans les données.")
        return

    # Affichage des données sous forme de tableau
    st.subheader("Données des Produits")
    st.dataframe(data)

    # Graphique de la distribution des catégories
    st.subheader("Distribution des Catégories (sans 'Produit_Sans_Nom')")
    fig1 = px.histogram(data_filtered, x="Catégorie", title="Distribution des Catégories")
    st.plotly_chart(fig1)

    # Graphique de la distribution de l'énergie
    st.subheader("Distribution de l'Énergie (kcal pour 100g)")
    fig2 = px.histogram(data, x="Énergie (kcal pour 100g)", title="Distribution de l'Énergie")
    st.plotly_chart(fig2)

    # Graphique de la distribution des protéines
    st.subheader("Distribution des Protéines (g pour 100g)")
    fig3 = px.histogram(data, x="Protéines (g pour 100g)", title="Distribution des Protéines")
    st.plotly_chart(fig3)

    # Graphique de la distribution des glucides
    st.subheader("Distribution des Glucides (g pour 100g)")
    fig4 = px.histogram(data, x="Glucides (g pour 100g)", title="Distribution des Glucides")
    st.plotly_chart(fig4)

    # Graphique de la distribution des sucres
    st.subheader("Distribution des Sucres (g pour 100g)")
    fig5 = px.histogram(data, x="Sucres (g pour 100g)", title="Distribution des Sucres")
    st.plotly_chart(fig5)

    # Graphique de la distribution des lipides
    st.subheader("Distribution des Lipides (g pour 100g)")
    fig6 = px.histogram(data, x="Lipides (g pour 100g)", title="Distribution des Lipides")
    st.plotly_chart(fig6)

    # Graphique de la distribution des acides gras saturés
    st.subheader("Distribution des Acides gras saturés (g pour 100g)")
    fig7 = px.histogram(data, x="Acides gras saturés (g pour 100g)", title="Distribution des Acides gras saturés")
    st.plotly_chart(fig7)

    # Graphique de la distribution du sel
    st.subheader("Distribution du Sel (g pour 100g)")
    fig8 = px.histogram(data, x="Sel (g pour 100g)", title="Distribution du Sel")
    st.plotly_chart(fig8)

    # Graphique des scores normalisés
    st.subheader("Distribution des Scores Normalisés")
    fig9 = px.histogram(data, x="Normalized Score", title="Distribution des Scores Normalisés")
    st.plotly_chart(fig9)

    # Scatter plot de l'énergie contre les protéines
    st.subheader("Énergie vs Protéines")
    fig10 = px.scatter(data, x="Énergie (kcal pour 100g)", y="Protéines (g pour 100g)", color="Catégorie", title="Énergie vs Protéines")
    st.plotly_chart(fig10)

    # Scatter plot des glucides contre les sucres
    st.subheader("Glucides vs Sucres")
    fig11 = px.scatter(data, x="Glucides (g pour 100g)", y="Sucres (g pour 100g)", color="Catégorie", title="Glucides vs Sucres")
    st.plotly_chart(fig11)

    # Box plot de l'énergie par catégorie
    st.subheader("Box Plot de l'Énergie par Catégorie")
    fig12 = px.box(data_filtered, x="Catégorie", y="Énergie (kcal pour 100g)", title="Box Plot de l'Énergie par Catégorie")
    st.plotly_chart(fig12)

    # Violin plot des protéines par catégorie
    st.subheader("Violin Plot des Protéines par Catégorie")
    fig13 = px.violin(data_filtered, x="Catégorie", y="Protéines (g pour 100g)", box=True, points="all", title="Violin Plot des Protéines par Catégorie")
    st.plotly_chart(fig13)