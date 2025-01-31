import streamlit as st
import os

from generateur_en import design_potion, export_potion, roll_potion, TABLES
from kpi import initialize_logs, log_potion

st.set_page_config(
    page_title="DnD Potion Generator", 
    page_icon="🧙‍♂️", 
    layout="wide",
    initial_sidebar_state="expanded"
    )

if not os.path.exists("logs/logs.csv"):
    initialize_logs()

st.markdown("""
<h1 style="text-align: center;">🧙‍♂️ DnD Potion Generator</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; font-size: 0.9em; font-style: italic;">
    <strong style="color: #922610; font-weight: bold;">Not all potions have labels</strong>, and drinking a mysterious liquid can be very dangerous... Or it could save your life!
    <br>
    This generator allows DMs to create random and procedural potions with amazing effects for their players. Have fun!
</div>
""", unsafe_allow_html=True)

# Initialize session state if it doesn't exist
if 'en_potions' not in st.session_state:
    st.session_state.en_potions = []

pin = st.sidebar.number_input("Number of ingredients", 0, 99999, 0)

radio = st.sidebar.radio("Mode", ["Generation", "Selection"], horizontal=True)

if radio == "Generation":
    col_left, col_container, col_right = st.columns([1, 3, 1])
    
    with col_left:
        pass
        
    with col_right:
        pass

    with col_container:
        nb_potions = st.sidebar.slider("Number of potions", 1, 10 if pin != 8565 else 3, 1)

        if pin == 8565:
            type_titre = st.sidebar.selectbox("Title", ["Procedural", "AI"])
        else:
            type_titre = "Procedural"

        generate_button = st.sidebar.button("Generate a potion")

        if generate_button:
            # Clear previous potions list
            st.session_state.en_potions = []
            
            for _ in range(nb_potions):
                potion_variables = roll_potion()
                potion, titre = design_potion(potion_variables, type_titre)
                export_potion(potion, titre)
                log_potion("en", type_titre, titre, potion_variables)
                st.divider()
                st.html(potion)
                st.download_button(
                    label="Download",
                    data=open(f"potion_images/{titre.replace(' ', '_')}.png", "rb").read(),
                    file_name=f"{titre.replace(' ', '_')}.png",
                    mime="image/png"
                )
                # Store potion data in session state
                st.session_state.en_potions.append({
                    'html': potion,
                    'titre': titre,
                    'image': open(f"potion_images/{titre.replace(' ', '_')}.png", "rb").read()
                })

        else:
            # Display potions stored in session state
            for potion_data in st.session_state.en_potions:
                st.divider()
                st.html(potion_data['html'])
                export_potion(potion_data['html'], potion_data['titre'])
                st.download_button(
                    label="Download",
                    data=potion_data['image'],
                    file_name=f"{potion_data['titre'].replace(' ', '_')}.png",
                    mime="image/png",
                    key=f"download_{potion_data['titre']}"
                )
else:
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    custom_title = st.text_input("Custom title (optional)", "")
    
    with col1:
        name = st.selectbox("Potion type", TABLES["titres"])
        container = st.selectbox("Container", TABLES["conteneurs"], index=0)
        main_appearance = st.selectbox("Main appearance", TABLES["apparences_principales"], index=3)
        with_appearance = st.selectbox("Additional appearance", TABLES["apparences_avec"], index=8)
        
    with col2:
        texture = st.selectbox("Texture", TABLES["textures"], index=0)
        taste = st.selectbox("Taste", TABLES["gouts_odeurs"], index=3)
        smell = st.selectbox("Smell", TABLES["gouts_odeurs"], index=4)
        label = st.selectbox("Label", TABLES["etiquettes"], index=0)
    
    with col3:
        intensity = st.selectbox("Intensity", [i[0] for i in TABLES["intensite"]])
        
        if intensity == "Legendary":
            max_main_effects = 3
        elif intensity == "Strong":
            max_main_effects = 2
        else:
            max_main_effects = 1
            
        main_effects = st.multiselect(f"Main effects ({max_main_effects})", TABLES["effets_principaux"], default=["Healing. It instantly regenerates some health when drank."], max_selections=max_main_effects)
        
        toxicity = st.selectbox("Toxicity", [i[0] for i in TABLES["toxicite"]])
        
        if toxicity == "Cursed":
            max_side_effects = 3
        elif toxicity == "Flayed":
            max_side_effects = 2
        elif toxicity == "Rotten":
            max_side_effects = 1
        else:
            max_side_effects = 0
            
        if max_side_effects > 0:
            side_effects = st.multiselect(f"Side effects ({max_side_effects})", TABLES["effets_secondaires"], max_selections=max_side_effects)
        else:
            side_effects = []
        
        special = st.selectbox("Special", [i[0] for i in TABLES["special"]], index=0)
    
    for i in TABLES["special"]:
        if i[0] == special:
            special_effect = i[1]
            break

    potion_variables = {
        "nom": name,
        "conteneur": container,
        "apparence_principale": main_appearance,
        "apparence_avec": with_appearance,
        "texture": texture,
        "gout": taste,
        "odeur": smell,
        "etiquette": label,
        "intensite_name": intensity,
        "toxicite_name": toxicity,
        "special_name": special,
        "special_effect": special_effect,
        "effets_principaux": main_effects,
        "effets_secondaires": side_effects
    }

    potion, titre = design_potion(potion_variables, custom_title if custom_title else "Procedural")
    st.divider()
    st.html(potion)
    generate_button = st.button("Generate")
    if generate_button:
        export_potion(potion, titre)
        log_potion("en", ("Personnalisé" if custom_title else "Procedural"), titre, potion_variables)
        st.download_button(
            label="Download",
            data=open(f"potion_images/{titre.replace(' ', '_')}.png", "rb").read(),
            file_name=f"{titre.replace(' ', '_')}.png",
            mime="image/png"
        )

st.sidebar.divider()
st.sidebar.caption("Generator by [NicolasBchb - Datalgo](https://x.com/nicolasbchb)")
st.sidebar.caption("The potion characteristics are based on the excellent work of [Olirant](https://www.reddit.com/user/olirant/) from this [Reddit post](https://www.reddit.com/r/DnDBehindTheScreen/comments/4btnkc/random_potions_table/).")