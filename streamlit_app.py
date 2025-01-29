import streamlit as st

from generateur import design_potion, export_potion, roll_potion, TABLES

st.set_page_config(page_title="Générateur de potion DnD", page_icon="🧙‍♂️", layout="wide")

st.title("🧙‍♂️ Générateur de potion DnD")

# Initialiser le session state s'il n'existe pas
if 'potions' not in st.session_state:
    st.session_state.potions = []

pin = st.sidebar.number_input("Nombre d'ingrédients", 0, 9999, 0)

if pin == 8565:
    radio = st.sidebar.radio("Mode", ["Génération", "Sélection"], horizontal=True)
    
    if radio == "Génération":
        nb_potions = st.sidebar.slider("Nombre de potions", 1, 10, 1)

        type_titre = st.sidebar.selectbox("Titre", ["Procedural", "AI"])

        generate_button = st.sidebar.button("Générer une potion")

        if generate_button:
            # Vider la liste des potions précédentes
            st.session_state.potions = []
            
            for _ in range(nb_potions):
                potion_variables = roll_potion()
                potion, titre = design_potion(potion_variables, type_titre)
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
    else:
        col1, col2, col3 = st.columns(3)
        
        titre_personnalise = st.text_input("Titre personnalisé (optionnel)", "")
        
        with col1:
            nom = st.selectbox("Type de potion", TABLES["titres"])
            conteneur = st.selectbox("Conteneur", TABLES["conteneurs"])
            apparence_principale = st.selectbox("Apparence principale", TABLES["apparences_principales"])
            apparence_avec = st.selectbox("Apparence avec", TABLES["apparences_avec"])
            
        with col2:
            texture = st.selectbox("Texture", TABLES["textures"])
            gout = st.selectbox("Gout", TABLES["gouts_odeurs"])
            odeur = st.selectbox("Odeur", TABLES["gouts_odeurs"])
            etiquette = st.selectbox("Etiquette", TABLES["etiquettes"])
        
        with col3:
            intensite = st.selectbox("Intensité", [i[0] for i in TABLES["intensite"]])
            
            if intensite == "Légendaire":
                max_effets_principaux = 3
            elif intensite == "Puissant":
                max_effets_principaux = 2
            else:
                max_effets_principaux = 1
                
            effets_principaux = st.multiselect(f"Effets principaux ({max_effets_principaux})", TABLES["effets_principaux"], max_selections=max_effets_principaux)
            
            toxicite = st.selectbox("Toxicité", [i[0] for i in TABLES["toxicite"]])
            
            if toxicite == "Maudit":
                max_effets_secondaires = 3
            elif toxicite == "Frelaté":
                max_effets_secondaires = 2
            elif toxicite == "Périmé":
                max_effets_secondaires = 1
            else:
                max_effets_secondaires = 0
                
            if max_effets_secondaires > 0:
                effets_secondaires = st.multiselect(f"Effets secondaires ({max_effets_secondaires})", TABLES["effets_secondaires"], max_selections=max_effets_secondaires)
            else:
                effets_secondaires = []
            
            special = st.selectbox("Spécial", [i[0] for i in TABLES["special"]], index=0)
        
        for i in TABLES["special"]:
            if i[0] == special:
                special_effect = i[1]
                break

        potion_variables = {
            "nom": nom,
            "conteneur": conteneur,
            "apparence_principale": apparence_principale,
            "apparence_avec": apparence_avec,
            "texture": texture,
            "gout": gout,
            "odeur": odeur,
            "etiquette": etiquette,
            "intensite_name": intensite,
            # "intensite_effect": intensite_effect,
            "toxicite_name": toxicite,
            # "toxicite_effect": toxicite_effect,
            "special_name": special,
            "special_effect": special_effect,
            "effets_principaux": effets_principaux,
            "effets_secondaires": effets_secondaires
        }

        potion, titre = design_potion(potion_variables, titre_personnalise if titre_personnalise else "Procedural")
        st.divider()
        st.html(potion)
        # export_potion(potion, titre)
        # st.download_button(
        #     label="Télécharger",
        #     data=open(f"potion_images/{titre.replace(' ', '_')}.png", "rb").read(),
        #     file_name=f"{titre.replace(' ', '_')}.png",
        #     mime="image/png"
        # )

# {
#     "nom": random.choice(TABLES["titres"]),
#     "conteneur": random.choice(TABLES["conteneurs"]),
#     "apparence_principale": random.choice(TABLES["apparences_principales"]),
#     "apparence_avec": random.choice(TABLES["apparences_avec"]),
#     "texture": random.choice(TABLES["textures"]),
#     "gout": random.choice(TABLES["gouts_odeurs"]),
#     "odeur": random.choice(TABLES["gouts_odeurs"]),
#     "etiquette": random.choice(TABLES["etiquettes"]),
#     "effet_principal": random.choice(TABLES["effets_principaux"]),
#     "intensite_name": intensite_name,
#     "intensite_effect": intensite_effect,
#     "toxicite_name": toxicite_name,
#     "toxicite_effect": toxicite_effect,
#     "special_name": special_name,
#     "special_effect": special_effect,
#     "effets_principaux": effets_principaux_list,
#     "effets_secondaires": effets_secondaires_list,
# }