import streamlit as st

from generateur import generer_potion

st.set_page_config(page_title="Générateur de potion DnD", page_icon="🧙‍♂️")

st.title("🧙‍♂️ Générateur de potion DnD")

pin = st.sidebar.number_input("Nombre d'ingrédients", 0, 9999, 0)

if pin == 1234:
    nb_potions = st.sidebar.slider("Nombre de potions", 1, 10, 1)

    type_titre = st.sidebar.selectbox("Titre", ["Procedural", "AI"])

    generate_button = st.sidebar.button("Générer une potion")

    if generate_button:
        for _ in range(nb_potions):
            potion = generer_potion(type_titre)
            st.divider()
            st.write(potion)
