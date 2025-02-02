import streamlit as st
import os
import json
from generateur import Potion, initialize_logs


st.set_page_config(
    page_title="Générateur de potions DnD",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Charger les textes
with open("l10n/texts.json", "r", encoding="utf-8") as f:
    texts = json.load(f)

langue = st.sidebar.radio("Language", ["🇫🇷", "🇬🇧"], horizontal=True, label_visibility="hidden")
lang = "fr" if langue == "🇫🇷" else "en"
t = texts[lang]  # Obtenir les textes pour la langue sélectionnée

st.markdown(
    f"""
<h1 style="text-align: center;">🧙‍♂️ {t['title']}</h1>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div style="text-align: center; font-size: 0.9em; font-style: italic;">
    <strong style="color: #922610; font-weight: bold;">{t['subtitle']}</strong>
    <br>
    {t['description']}
</div>
""",
    unsafe_allow_html=True,
)

# Initialiser le session state s'il n'existe pas
if "fr_potions" not in st.session_state:
    st.session_state.fr_potions = []

if not os.path.exists("logs/logs.csv"):
    initialize_logs()


pin = st.sidebar.number_input(t["ingredients_number"], 0, 99999, 0)

radio = st.sidebar.radio(t["mode"], [t["generation"], t["selection"]], horizontal=True)

if radio == t["generation"]:
    col_left, col_container, col_right = st.columns([1, 4, 1])

    with col_left:
        pass

    with col_right:
        pass

    with col_container:
        nb_potions = st.sidebar.slider(
            t["potions_number"], 1, 10 if pin != 8565 else 3, 1
        )

        if pin == 8565:
            type_titre = st.sidebar.selectbox("Titre", ["Procedural", "AI"])
        else:
            type_titre = "Procedural"

        generate_button = st.sidebar.button(t["generate_button"])

        if generate_button:
            # Vider la liste des potions précédentes
            st.session_state.fr_potions = []

            for _ in range(nb_potions):
                potion = Potion(lang=lang)
                potion.roll()
                potion.design_potion(title_type=type_titre)
                potion.save_potion_log(type_titre)
                st.divider()
                st.html(potion.html)
                # st.download_button(
                #     label="Télécharger",
                #     data=open(f"potion_images/{potion.titre.replace(' ', '_')}.png", "rb").read(),
                #     file_name=f"{potion.titre.replace(' ', '_')}.png",
                #     mime="image/png"
                # )
                # Stocker les données de la potion dans le session state
                st.session_state.fr_potions.append(potion)

        else:
            # Afficher les potions stockées dans le session state
            for potion in st.session_state.fr_potions:
                st.divider()
                st.html(potion.html)
                # st.download_button(
                #     label="Télécharger",
                #     data=open(f"potion_images/{potion.titre.replace(' ', '_')}.png", "rb").read(),
                #     file_name=f"{potion.titre.replace(' ', '_')}.png",
                #     mime="image/png",
                #     key=f"download_{potion.titre}"
                # )
else:
    st.divider()

    TABLES = {
        "titles": json.load(open(f"l10n/{lang}/tables/titles.json")),
        "containers": json.load(open(f"l10n/{lang}/tables/containers.json")),
        "main_appearances": json.load(
            open(f"l10n/{lang}/tables/main_appearances.json")
        ),
        "with_appearances": json.load(
            open(f"l10n/{lang}/tables/with_appearances.json")
        ),
        "textures": json.load(open(f"l10n/{lang}/tables/textures.json")),
        "tastes_smells": json.load(open(f"l10n/{lang}/tables/tastes_smells.json")),
        "labels": json.load(open(f"l10n/{lang}/tables/labels.json")),
        "intensities": json.load(open(f"l10n/{lang}/tables/intensities.json")),
        "toxicities": json.load(open(f"l10n/{lang}/tables/toxicities.json")),
        "specials": json.load(open(f"l10n/{lang}/tables/specials.json")),
        "main_effects": json.load(open(f"l10n/{lang}/tables/main_effects.json")),
        "side_effects": json.load(open(f"l10n/{lang}/tables/side_effects.json")),
    }

    potion = Potion(lang=lang)

    col1, col2, col3 = st.columns(3)

    titre_personnalise = st.text_input(t["custom_title"], "")

    with col1:
        potion.type = st.selectbox(t["potion_attributes"]["type"], TABLES["titles"])
        potion.container = st.selectbox(
            t["potion_attributes"]["container"], TABLES["containers"], index=0
        )
        potion.main_appearance = st.selectbox(
            t["potion_attributes"]["main_appearance"],
            TABLES["main_appearances"],
            index=3,
        )
        potion.with_appearance = st.selectbox(
            t["potion_attributes"]["with_appearance"],
            TABLES["with_appearances"],
            index=8,
        )

    with col2:
        potion.texture = st.selectbox(
            t["potion_attributes"]["texture"], TABLES["textures"], index=0
        )
        potion.taste = st.selectbox(
            t["potion_attributes"]["taste"], TABLES["tastes_smells"], index=3
        )
        potion.smell = st.selectbox(
            t["potion_attributes"]["smell"], TABLES["tastes_smells"], index=4
        )
        potion.label = st.selectbox(
            t["potion_attributes"]["label"], TABLES["labels"], index=0
        )

    with col3:
        potion.intensity = st.selectbox(
            t["potion_attributes"]["intensity"],
            TABLES["intensities"],
            format_func=lambda x: x["name"],
        )

        potion.main_effects = st.multiselect(
            f"{t['potion_attributes']['main_effects']} ({potion.intensity['nb_effects']})",
            TABLES["main_effects"],
            # default=[TABLES["main_effects"][0]],
            max_selections=potion.intensity["nb_effects"],
            format_func=lambda x: x["name"],
        )

        potion.toxicity = st.selectbox(
            t["potion_attributes"]["toxicity"],
            TABLES["toxicities"],
            format_func=lambda x: x["name"],
        )

        if potion.toxicity["nb_effects"] > 0:
            potion.side_effects = st.multiselect(
                f"{t['potion_attributes']['side_effects']} ({potion.toxicity['nb_effects']})",
                TABLES["side_effects"],
                # default=[TABLES["side_effects"][0]],
                max_selections=potion.toxicity["nb_effects"],
                format_func=lambda x: x["name"],
            )
        else:
            potion.side_effects = []

        potion.special = st.selectbox(
            t["potion_attributes"]["special"],
            TABLES["specials"],
            format_func=lambda x: x["name"],
            index=0,
        )

    potion.design_potion(
        title_type=titre_personnalise if titre_personnalise else "Procedural"
    )
    st.divider()
    st.html(potion.html)
    # generate_button = st.button("Générer")
    # if generate_button:
    # potion.save_potion_log("fr", ("Personnalisé" if titre_personnalise else "Procedural"))
    # st.download_button(
    #     label="Télécharger",
    #     data=open(f"potion_images/{potion.titre.replace(' ', '_')}.png", "rb").read(),
    #     file_name=f"{potion.titre.replace(' ', '_')}.png",
    #     mime="image/png"
    # )

st.sidebar.divider()
st.sidebar.caption(t["footer"]["developed_by"])
st.sidebar.caption(t["footer"]["credits"])
