import streamlit as st
import os

from generateur import design_potion, export_potion, roll_potion, TABLES
from kpi import initialize_logs, log_potion
st.set_page_config(
    page_title="Générateur de potions DnD", 
    page_icon="🧙‍♂️", 
    layout="wide",
    initial_sidebar_state="expanded"
    )

st.markdown("""
<h1 style="text-align: center;">🧙‍♂️ Générateur de potions DnD</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; font-size: 0.9em; font-style: italic;">
    <strong style="color: #922610; font-weight: bold;">Toutes les potions n'ont pas d'étiquettes</strong>, et boire un liquide mystérieux pourrait s'avèrer très dangereux... Ou cela pourrait vous sauver la vie !
    <br>
    Ce générateur permet aux MJs de créer des potions aléatoires et procédurales avec des effets incroyables pour leurs joueurs. Amusez-vous bien !
</div>
""", unsafe_allow_html=True)

# Initialiser le session state s'il n'existe pas
if 'fr_potions' not in st.session_state:
    st.session_state.fr_potions = []
    
if not os.path.exists("logs/logs.csv"):
    initialize_logs()

pin = st.sidebar.number_input("Nombre d'ingrédients", 0, 99999, 0)


radio = st.sidebar.radio("Mode", ["Génération", "Sélection"], horizontal=True)

if radio == "Génération":
    col_left, col_container, col_right = st.columns([1, 3, 1])
    
    with col_left:
        pass
        
    with col_right:
        pass

    with col_container:
        nb_potions = st.sidebar.slider("Nombre de potions", 1, 10 if pin != 8565 else 3, 1)

        if pin == 8565:
            type_titre = st.sidebar.selectbox("Titre", ["Procedural", "AI"])
        else:
            type_titre = "Procedural"

        generate_button = st.sidebar.button("Générer une potion")

        if generate_button:
            # Vider la liste des potions précédentes
            st.session_state.fr_potions = []
            
            for _ in range(nb_potions):
                potion_variables = roll_potion()
                potion, titre = design_potion(potion_variables, type_titre)
                export_potion(potion, titre)
                log_potion("fr", type_titre, titre, potion_variables)
                st.divider()
                st.html(potion)
                st.download_button(
                    label="Télécharger",
                    data=open(f"potion_images/{titre.replace(' ', '_')}.png", "rb").read(),
                    file_name=f"{titre.replace(' ', '_')}.png",
                    mime="image/png"
                )
                # Stocker les données de la potion dans le session state
                st.session_state.fr_potions.append({
                    'html': potion,
                    'titre': titre,
                    'image': open(f"potion_images/{titre.replace(' ', '_')}.png", "rb").read()
                })

        else:
            # Afficher les potions stockées dans le session state
            for potion_data in st.session_state.fr_potions:
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
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    titre_personnalise = st.text_input("Titre personnalisé (optionnel)", "")
    
    with col1:
        nom = st.selectbox("Type de potion", TABLES["titres"])
        conteneur = st.selectbox("Conteneur", TABLES["conteneurs"], index=0)
        apparence_principale = st.selectbox("Apparence principale", TABLES["apparences_principales"], index=3)
        apparence_avec = st.selectbox("Apparence avec", TABLES["apparences_avec"], index=8)
        
    with col2:
        texture = st.selectbox("Texture", TABLES["textures"], index=0)
        gout = st.selectbox("Gout", TABLES["gouts_odeurs"], index=3)
        odeur = st.selectbox("Odeur", TABLES["gouts_odeurs"], index=4)
        etiquette = st.selectbox("Etiquette", TABLES["etiquettes"], index=0)
    
    with col3:
        intensite = st.selectbox("Intensité", [i[0] for i in TABLES["intensite"]])
        
        if intensite == "Légendaire":
            max_effets_principaux = 3
        elif intensite == "Puissant":
            max_effets_principaux = 2
        else:
            max_effets_principaux = 1
            
        effets_principaux = st.multiselect(f"Effets principaux ({max_effets_principaux})", TABLES["effets_principaux"], default=["Soin. Régénère instantanément des points de vie lorsqu'elle est bue. Régénère 2d6+4 PV."], max_selections=max_effets_principaux)
        
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
        "toxicite_name": toxicite,
        "special_name": special,
        "special_effect": special_effect,
        "effets_principaux": effets_principaux,
        "effets_secondaires": effets_secondaires
    }

    potion, titre = design_potion(potion_variables, titre_personnalise if titre_personnalise else "Procedural")
    st.divider()
    st.html(potion)
    generate_button = st.button("Générer")
    if generate_button:
        log_potion("fr", ("Personnalisé" if titre_personnalise else "Procedural"), titre, potion_variables)
        export_potion(potion, titre)
        st.download_button(
            label="Télécharger",
            data=open(f"potion_images/{titre.replace(' ', '_')}.png", "rb").read(),
            file_name=f"{titre.replace(' ', '_')}.png",
            mime="image/png"
        )
        
st.sidebar.divider()
st.sidebar.caption("Ce generateur est développé par [Nicolas Bouchaib - Datalgo](https://x.com/nicolasbchb)")
st.sidebar.caption("Les caractéristiques des potions sont basées sur le super travail d'[Olirant](https://www.reddit.com/user/olirant/) dans ce [post Reddit](https://www.reddit.com/r/DnDBehindTheScreen/comments/4btnkc/random_potions_table/).")
