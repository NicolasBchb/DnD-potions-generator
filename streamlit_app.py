import streamlit as st

from generateur import generer_potion, export_potion

st.set_page_config(page_title="Générateur de potion DnD", page_icon="🧙‍♂️")

st.title("🧙‍♂️ Générateur de potion DnD")

# Initialiser le session state s'il n'existe pas
if 'potions' not in st.session_state:
    st.session_state.potions = []

pin = st.sidebar.number_input("Nombre d'ingrédients", 0, 9999, 0)

if pin == 1234:
    nb_potions = st.sidebar.slider("Nombre de potions", 1, 10, 1)

    type_titre = st.sidebar.selectbox("Titre", ["Procedural", "AI"])

    generate_button = st.sidebar.button("Générer une potion")

    if generate_button:
        # Vider la liste des potions précédentes
        st.session_state.potions = []
        
        for _ in range(nb_potions):
            potion, titre = generer_potion(type_titre)
            export_potion(potion, titre)
            st.divider()
            st.html(potion)
            st.download_button(
                label="Télécharger",
                data=open(f"potion_images/{titre.replace(' ', '_')}.png", "rb").read(),
                file_name=f"{titre.replace(' ', '_')}.png",
                mime="image/png"
            )
            # Stocker les données de la potion dans le session state
            st.session_state.potions.append({
                'html': potion,
                'titre': titre,
                'image': open(f"potion_images/{titre.replace(' ', '_')}.png", "rb").read()
            })


    else:
        # Afficher les potions stockées dans le session state
        for potion_data in st.session_state.potions:
            st.divider()
            st.html(potion_data['html'])
            export_potion(potion_data['html'], potion_data['titre'])
            st.download_button(
                label="Télécharger",
                data=potion_data['image'],
                file_name=f"{potion_data['titre'].replace(' ', '_')}.png",
                mime="image/png",
                key=f"download_{potion_data['titre']}"
            )
