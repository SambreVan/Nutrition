import streamlit as st

def calculate_bmr(weight, height, age, sex):
    if sex == "Homme":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def calculate_tdee(bmr, activity_level):
    return bmr * activity_level

def show_nutrition_calculator_page():
    st.subheader("Calculateur de l'IMC, des calories nécessaires et de la répartition des macronutriments.")

    weight = st.number_input("Poids (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
    height = st.number_input("Taille (cm)", min_value=100.0, max_value=250.0, value=175.0, step=1.0)
    age = st.number_input("Âge", min_value=12, max_value=100, value=30, step=1)
    sex = st.selectbox("Sexe", ["Homme", "Femme"])
    activity_level = st.selectbox("Niveau d'activité physique", 
                                  options=["Sédentaire", "Légèrement actif", "Modérément actif", "Très actif", "Extrêmement actif"],
                                  format_func=lambda x: {"Sédentaire": "Peu ou pas d'exercice",
                                                         "Légèrement actif": "Exercice léger/sport 1-3 jours/semaine",
                                                         "Modérément actif": "Exercice modéré/sport 3-5 jours/semaine",
                                                         "Très actif": "Exercice dur/sport 6-7 jours/semaine",
                                                         "Extrêmement actif": "Exercice très dur/physique travail + exercice physique"}[x])

    activity_factors = {
        "Sédentaire": 1.2,
        "Légèrement actif": 1.375,
        "Modérément actif": 1.55,
        "Très actif": 1.725,
        "Extrêmement actif": 1.9
    }

    if st.button("Calculer"):
        bmr = calculate_bmr(weight, height, age, sex)
        tdee = calculate_tdee(bmr, activity_factors[activity_level])
        st.write(f"Votre BMR (Basal Metabolic Rate): {bmr:.2f} calories/jour")
        st.write(f"Votre TDEE (Total Daily Energy Expenditure): {tdee:.2f} calories/jour")

        
        st.write("Répartition recommandée des macronutriments:")
        st.write(f"Protéines: {tdee * 0.3 / 4:.2f} g (30% des calories)")
        st.write(f"Glucides: {tdee * 0.4 / 4:.2f} g (40% des calories)")
        st.write(f"Lipides: {tdee * 0.3 / 9:.2f} g (30% des calories)")
