import streamlit as st
import pandas as pd
import sqlite3
import bcrypt
import os
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from nutrition import show_prediction_page as show_nutrition_page
from imc import show_nutrition_calculator_page as show_calculator_page
from profile_page import show_profile_page
from db_management import create_tables, add_userdata, login_user, get_user_data, save_image, get_latest_weight
from analysis_page import show_analysis_page

def connect_db():
    return sqlite3.connect('users.db')

def create_weight_table():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS weight_tracking(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                date TEXT,
                weight REAL,
                FOREIGN KEY(username) REFERENCES users(username)
            )
        ''')
        conn.commit()

def add_weight_data(username, date, weight):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO weight_tracking(username, date, weight)
            VALUES (?, ?, ?)
        ''', (username, date, weight))
        conn.commit()

def get_weight_data(username):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT date, weight FROM weight_tracking WHERE username = ? ORDER BY date
        ''', (username,))
        data = c.fetchall()
    return data

def show_weight_tracking_page():
    st.subheader("Suivi du Poids")

    if 'username' not in st.session_state or not st.session_state['username']:
        st.warning("Veuillez vous connecter pour suivre votre poids.")
        return

    username = st.session_state['username']

    date = st.date_input("Date")
    weight = st.number_input("Poids (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)

    if st.button("Ajouter"):
        add_weight_data(username, date.strftime('%Y-%m-%d'), weight)
        st.success("Entrée ajoutée avec succès.")

    weight_data = get_weight_data(username)
    if weight_data:
        dates, weights = zip(*weight_data)
        fig = px.line(x=dates, y=weights, markers=True, labels={'x': 'Date', 'y': 'Poids (kg)'}, title='Courbe de progression du poids')
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="date"))
        st.plotly_chart(fig)
    else:
        st.info("Aucune donnée de poids disponible.")

def show_home_page():
    st.title("Bienvenue sur notre site de suivi nutritionnel")
    st.write("""
        Notre site vous aide à en savoir plus sur ce que vous mangez et à mieux gérer votre nutrition quotidienne.
        Vous pouvez suivre vos macronutriments, votre poids, et obtenir des analyses détaillées sur vos choix alimentaires.
    """)

    st.subheader("L'importance des macronutriments")
    st.write("""
        **Protéines :**
        Les protéines sont essentielles pour la construction et la réparation des tissus corporels. Elles jouent également un rôle crucial dans la production d'enzymes et d'hormones.
        Une consommation quotidienne de 50g de protéines est recommandée pour un adulte moyen.
    """)

    st.write("""
        **Glucides :**
        Les glucides sont la principale source d'énergie de votre corps. Ils se divisent en glucides simples et complexes, chacun ayant un impact différent sur votre glycémie.
        Une consommation quotidienne de 275g de glucides est recommandée pour un adulte moyen.
    """)

    st.write("""
        **Lipides :**
        Les lipides, ou graisses, sont importants pour stocker l'énergie, isoler et protéger vos organes, et faciliter l'absorption des vitamines liposolubles.
        Une consommation quotidienne de 70g de lipides est recommandée pour un adulte moyen.
    """)

    st.image("https://images.unsplash.com/photo-1606787366850-de6330128bfc?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="Une alimentation équilibrée est la clé d'une vie saine.")

    # Graphique de répartition des macronutriments
    macronutriments = {'Protéines': 50, 'Glucides': 275, 'Lipides': 70}
    fig1 = px.pie(values=macronutriments.values(), names=macronutriments.keys(), title="Répartition recommandée des macronutriments (g/jour)")
    st.plotly_chart(fig1)

    # Graphique de consommation calorique
    calories = {'Petit-déjeuner': 300, 'Déjeuner': 500, 'Dîner': 600, 'Collations': 200}
    fig2 = px.bar(x=calories.keys(), y=calories.values(), title="Répartition de la consommation calorique (kcal)")
    st.plotly_chart(fig2)

    # Graphique de consommation moyenne de fibres
    fibres = {'Age 18-25': 30, 'Age 26-35': 28, 'Age 36-45': 25, 'Age 46-55': 23, 'Age 56-65': 21, 'Age 66-75': 20}
    fig3 = px.bar(x=fibres.keys(), y=fibres.values(), title="Consommation moyenne de fibres par groupe d'âge (g/jour)")
    st.plotly_chart(fig3)

    # Graphique de répartition des macronutriments par groupe d'âge
    ages = ['18-25', '26-35', '36-45', '46-55', '56-65', '66-75']
    macronutriments_by_age = {
        'Protéines': [55, 53, 50, 48, 45, 43],
        'Glucides': [300, 290, 280, 270, 260, 250],
        'Lipides': [75, 70, 68, 65, 63, 60]
    }
    df_macronutrients = pd.DataFrame(macronutriments_by_age, index=ages)
    fig4 = px.bar(df_macronutrients, barmode='group', title="Répartition des macronutriments par groupe d'âge (g/jour)")
    st.plotly_chart(fig4)

    # Graphique de l'impact des macronutriments sur l'IMC
    imc_data = {
        'Protéines': [20, 22, 25, 23, 21, 24, 26],
        'Glucides': [50, 55, 60, 58, 57, 59, 61],
        'Lipides': [30, 28, 25, 27, 29, 26, 24],
        'IMC': [22, 23, 24, 23.5, 24.2, 24.7, 25]
    }
    df_imc = pd.DataFrame(imc_data)
    fig5 = px.scatter_matrix(df_imc, dimensions=['Protéines', 'Glucides', 'Lipides'], color='IMC', title="Impact des macronutriments sur l'IMC")
    st.plotly_chart(fig5)

    # Graphique de distribution des types de repas
    meal_types = {'Petit-déjeuner': 30, 'Déjeuner': 50, 'Dîner': 60, 'Collations': 40}
    fig6 = px.pie(values=meal_types.values(), names=meal_types.keys(), title="Distribution des types de repas")
    st.plotly_chart(fig6)

    # Graphique de comparaison des apports caloriques recommandés par sexe
    ages = [18, 25, 35, 45, 55, 65, 75]
    calories_men = [2500, 2400, 2300, 2200, 2100, 2000, 1900]
    calories_women = [2000, 1900, 1800, 1700, 1600, 1500, 1400]
    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(x=ages, y=calories_men, mode='lines+markers', name='Hommes'))
    fig7.add_trace(go.Scatter(x=ages, y=calories_women, mode='lines+markers', name='Femmes'))
    fig7.update_layout(title="Comparaison des apports caloriques recommandés par sexe (kcal/jour)", xaxis_title="Âge", yaxis_title="Calories")
    st.plotly_chart(fig7)

    # Statistiques sur la nutrition
    st.write("""
        **Statistiques sur la nutrition :**
        - En moyenne, un adulte consomme 2000 à 2500 kcal par jour.
        - Les protéines devraient représenter 10 à 35% de l'apport calorique total.
        - Les glucides devraient représenter 45 à 65% de l'apport calorique total.
        - Les lipides devraient représenter 20 à 35% de l'apport calorique total.
        - L'apport quotidien en fibres recommandé est de 25 à 30g.
        - La consommation excessive de sucre est liée à un risque accru de diabète et de maladies cardiovasculaires.
    """)

def show_login_page():
    st.subheader("Section de Connexion")
    st.write("Veuillez entrer vos informations pour vous connecter.")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type='password')
    if st.button("Connexion"):
        user = login_user(username, password)
        if user:
            st.session_state['username'] = username
            st.success(f"Connecté en tant que {username}")
            st.experimental_rerun()
        else:
            st.warning("Nom d'utilisateur ou mot de passe incorrect")

def show_signup_page():
    st.subheader("Créer un Nouveau Compte")
    st.write("Remplissez les informations ci-dessous pour créer un nouveau compte.")
    new_user = st.text_input("Nom d'utilisateur")
    new_password = st.text_input("Mot de passe", type='password')
    first_name = st.text_input("Prénom")
    last_name = st.text_input("Nom de famille")
    age = st.number_input("Âge", min_value=18, max_value=100, step=1)
    sex = st.radio("Sexe", ("Homme", "Femme"))
    profile_image = st.file_uploader("Télécharger une image de profil", type=['jpg', 'png', 'jpeg'])

    if st.button("S'inscrire"):
        add_userdata(new_user, new_password, first_name, last_name, age, sex, profile_image)
        st.success("Compte créé avec succès")
        st.info("Allez dans la section de connexion pour vous connecter")

def show_static_data_page():
    st.title("Données Statistiques")
    st.write("Voici une série de graphiques pour illustrer les données statistiques.")
    
    # Afficher les images
    for i in range(1, 46):
        st.image(f"img/{i}.png", caption=f"Graphique {i}")

def main():
    create_tables()  
    st.sidebar.title("Navigation")

    # Gérer la connexion
    if 'username' not in st.session_state or not st.session_state['username']:
        choice = st.sidebar.selectbox("Aller à", ["Accueil", "Connexion", "Inscription"])
    else:
        username = st.session_state['username']
        user_data = get_user_data(username)
        if user_data:
            profile_image = user_data[7]
            if profile_image:
                st.sidebar.image(profile_image, width=100)
            st.sidebar.write(f"Connecté en tant que {username}")

        choice = st.sidebar.selectbox("Aller à", ["Accueil", "Profil", "Nutrition", "Calculateur", "Suivi du Poids", "Analyse", "Données Statistiques", "Déconnexion"])

    if choice == "Accueil":
        show_home_page()

    elif choice == "Connexion":
        show_login_page()

    elif choice == "Inscription":
        show_signup_page()

    elif choice == "Profil":
        show_profile_page()

    elif choice == "Nutrition":
        show_nutrition_page()

    elif choice == "Calculateur":
        show_calculator_page()

    elif choice == "Suivi du Poids":
        show_weight_tracking_page()

    elif choice == "Analyse":
        show_analysis_page()

    elif choice == "Données Statistiques":
        show_static_data_page()

    elif choice == "Déconnexion":
        if st.sidebar.button("Déconnexion"):
            del st.session_state['username']
            st.info("Vous avez été déconnecté.")
            st.experimental_rerun()

if __name__ == '__main__':
    main()
