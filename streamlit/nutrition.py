import streamlit as st
from joblib import load
import numpy as np

def show_prediction_page():
    st.subheader("Prédiction du Score Normalisé des Produits Alimentaires")


    model = load('gradient_boosting_model.joblib')
    

    st.write(f"Nombre de caractéristiques attendues: {model.n_features_in_}")


    energie = st.number_input('Énergie (kcal pour 100g)', min_value=0.0, value=0.0, format="%.2f")
    proteines = st.number_input('Protéines (g pour 100g)', min_value=0.0, value=0.0, format="%.2f")
    glucides = st.number_input('Glucides (g pour 100g)', min_value=0.0, value=0.0, format="%.2f")
    sucres = st.number_input('Sucres (g pour 100g)', min_value=0.0, value=0.0, format="%.2f")
    lipides = st.number_input('Lipides (g pour 100g)', min_value=0.0, value=0.0, format="%.2f")
    acides_gras = st.number_input('Acides gras saturés (g pour 100g)', min_value=0.0, value=0.0, format="%.2f")
    sel = st.number_input('Sel (g pour 100g)', min_value=0.0, value=0.0, format="%.2f")
    categorie = st.selectbox('Catégorie', ['alcoholic-beverages', 'sweets', 'cheeses', 'breads', 'snacks', 'soups', 'beverages'])


    if st.button('Prédire le Score'):
        
        features = np.zeros(model.n_features_in_)
        features[:7] = [energie, proteines, glucides, sucres, lipides, acides_gras, sel]
        categories_index = ['alcoholic-beverages', 'sweets', 'cheeses', 'breads', 'snacks', 'soups', 'beverages'].index(categorie)
        features[7 + categories_index] = 1  


        prediction = model.predict([features])
        score_pred = prediction[0]


        st.success(f'Le score prédit est: {score_pred:.2f}')
