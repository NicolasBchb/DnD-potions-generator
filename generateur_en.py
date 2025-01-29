import random
import re
import json

import dotenv
from openai import OpenAI

import imgkit

dotenv.load_dotenv()

TABLES = {
    "titres": json.load(open("tables/en/titres.json")),
    "conteneurs": json.load(open("tables/en/conteneurs.json")),
    "apparences_principales": json.load(open("tables/en/apparences_principales.json")),
    "apparences_avec": json.load(open("tables/en/apparences_avec.json")),
    "textures": json.load(open("tables/en/textures.json")),
    "gouts_odeurs": json.load(open("tables/en/gouts_odeurs.json")),
    "etiquettes": json.load(open("tables/en/etiquettes.json")),
    "effets_principaux": json.load(open("tables/en/effets_principaux.json")),
    "effets_secondaires": json.load(open("tables/en/effets_secondaires.json")),
    "intensite": [
        ("", "Normal power effect"),
        ("Strong", "Double effect"),
        ("Legendary", "Triple effect"),
    ],
    "toxicite": [
        ("", "No secondary effect."),
        ("Rotten", "Classic secondary effect."),
        ("Flayed", "Double secondary effect."),
        ("Cursed", "Triple secondary effect."),
    ],
    "special": [
        (
            "",
            "No special effect",
        ),
        (
            "Flashing",
            "The effect lasts only one instant, but its intensity is multiplied.",
        ),
        (
            "Delayed",
            "The effect is delayed by 1d6 rounds in combat or 1d20 minutes outside.",
        ),
        (
            "Eternal",
            "The effect is permanent. A 'Remove Curse' spell can remove it.",
        ),
    ],
}

def roll_potion():
    potion_variables = {
        "nom": random.choice(TABLES["titres"]),
        "conteneur": random.choice(TABLES["conteneurs"]),
        "apparence_principale": random.choice(TABLES["apparences_principales"]),
        "apparence_avec": random.choice(TABLES["apparences_avec"]),
        "texture": random.choice(TABLES["textures"]),
        "gout": random.choice(TABLES["gouts_odeurs"]),
        "odeur": random.choice(TABLES["gouts_odeurs"]),
        "etiquette": random.choice(TABLES["etiquettes"]),
    }

    intensite_name, intensite_effect = random.choices(
        TABLES["intensite"], weights=[60, 35, 5], k=1
    )[0]
    toxicite_name, toxicite_effect = random.choices(
        TABLES["toxicite"], weights=[30, 30, 15, 5], k=1
    )[0]
    special_name, special_effect = random.choices(
        TABLES["special"], weights=[79, 10, 10, 1], k=1
    )[0]

    # Générer le nombre approprié d'effets principaux
    nb_effets = 1
    if intensite_name == "Strong":
        nb_effets = 2
    elif intensite_name == "Legendary":
        nb_effets = 3
    effets_principaux_list = random.sample(TABLES["effets_principaux"], nb_effets)

    # Générer le nombre approprié d'effets secondaires
    nb_effets_secondaires = 0
    if toxicite_name == "Rotten":
        nb_effets_secondaires = 1
    elif toxicite_name == "Flayed":
        nb_effets_secondaires = 2
    elif toxicite_name == "Cursed":
        nb_effets_secondaires = 3
    effets_secondaires_list = (
        random.sample(TABLES["effets_secondaires"], nb_effets_secondaires)
        if nb_effets_secondaires > 0
        else []
    )

    potion_variables.update(
        {
            "intensite_name": intensite_name,
            "intensite_effect": intensite_effect,
            "toxicite_name": toxicite_name,
            "toxicite_effect": toxicite_effect,
            "special_name": special_name,
            "special_effect": special_effect,
            "effets_principaux": effets_principaux_list,
            "effets_secondaires": effets_secondaires_list,
        }
    )

    return potion_variables


def nettoyer(texte):
    # Liste des voyelles
    voyelles = "aeiouyAEIOUY"

    # On remplace uniquement "DE" suivi d'une voyelle par "D'"
    texte = re.sub(r"\bDE (?=[" + voyelles + r"])", "D'", texte)

    return texte


def titre_procedural(potion_variables):
    # Construire le titre avec tous les effets principaux
    effets_noms = " ".join(
        [effet.split(".")[0] for effet in potion_variables["effets_principaux"]]
    )

    return f"{potion_variables['nom']} {potion_variables['intensite_name']} of {effets_noms} {potion_variables['special_name']} {potion_variables['toxicite_name']}".capitalize()


def titre_ai(potion_variables):
    potion_description = {
        "nom": titre_procedural(potion_variables),
        "description": f"{potion_variables['conteneur']} contains a liquid {potion_variables['apparence_principale'].lower()} {potion_variables['texture'].lower()} with {potion_variables['apparence_avec'].lower()}. On top is {potion_variables['etiquette'].lower()}. Its smell reminds {potion_variables['odeur'].lower()} and its taste evokes {potion_variables['gout'].lower()}.",
        "effets_principaux": potion_variables["effets_principaux"],
        # "effets_secondaires": potion_variables["effets_secondaires"],
        "effets_speciaux": potion_variables["special_name"],
    }

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a DnD potion name generator. From the potion characteristics provided, you must generate a name evocative and metaphorical, without justification or formatting.",
            },
            {"role": "user", "content": json.dumps(potion_description)},
        ],
        max_tokens=50,
        temperature=0.9,
    )
    return completion.choices[0].message.content


def design_potion(potion_variables, type_titre="Procedural"):
    tags = [
        tag.capitalize()
        for tag in [
            potion_variables["intensite_name"],
            potion_variables["toxicite_name"],
            potion_variables["special_name"],
        ]
        if tag
    ]

    tags = f"""<div class="tags">{", ".join(tags)}</div>""" if tags else ""

    description_potion = f"""<div class="description">
    <h4>Description</h4>
    <p>{potion_variables['conteneur']} contains a {potion_variables['texture'].lower()} {potion_variables['apparence_principale'].lower()} liquid with {potion_variables['apparence_avec'].lower()}.</p>
    <p>The potion has a label showing {potion_variables['etiquette'].lower()}.</p>
    <p>Its smell reminds {potion_variables['odeur'].lower()} but its taste evokes {potion_variables['gout'].lower()}.</p>
</div>"""

    effets_principaux = """<div class="effets-principaux">
    <h4>Main effects</h4>
    <div class="property-block">"""

    # Ajouter tous les effets principaux
    for effet in potion_variables["effets_principaux"]:
        nom = effet.split(".")[0]
        description = effet[len(nom) + 1 :]
        effets_principaux += f"""
        <h5>{nom}</h5>
        <p>{description}</p>"""
    effets_principaux += "</div></div>"

    effets_secondaires = """<div class="effets-secondaires">
    <h4>Secondary effects</h4>
    <div class="property-block">"""

    for effet in potion_variables["effets_secondaires"]:
        nom = effet.split(". ")[0]
        description = effet[len(nom) + 1 :]
        effets_secondaires += f"""
        <h5>{nom}</h5>
        <p>{description}</p>"""
    effets_secondaires += "</div></div>"

    effets_speciaux = """<div class="effets-speciaux">
    <h4>Special effects</h4>
    <div class="property-block">"""

    if potion_variables["special_name"] != "":
        effets_speciaux += f"""
        <h5>{potion_variables['special_name'].capitalize()}</h5>
        <p>{potion_variables['special_effect']}</p>"""
    effets_speciaux += "</div></div>"

    potion = f"""<div class="stat-block">"""

    if type_titre == "Procedural":
        titre = titre_procedural(potion_variables)
    elif type_titre == "AI":
        titre = titre_ai(potion_variables)
    else:
        titre = type_titre

    potion += f"""<div class="creature-heading">
        <h1>{titre}</h1>
        {tags}
    </div>
    {description_potion}
    {effets_principaux}"""

    if potion_variables["effets_secondaires"] != []:
        potion += effets_secondaires
    if potion_variables["special_name"] != "":
        potion += effets_speciaux

    potion += "</div>"

    style = """
    <style>
    .stat-block {
        font-family: 'Noto Sans', 'Myriad Pro', Calibri, Helvetica, Arial, sans-serif;
        background: #FDF1DC;
        padding: 0.6em;
        border: 1px solid #DDD;
        box-shadow: 0 0 1.5em #867453;
        margin: 2em;
        border-radius: 10px;
        color: #222;
    }
    .stat-block h1 {
        font-family: 'Modesto Condensed', 'Libre Baskerville', 'Lora', 'Calisto MT', serif;
        color: #922610;
        font-size: 1.8em;
        line-height: 1.2em;
        margin: 10px 0 0;
        letter-spacing: 1px;
        font-variant: small-caps;
        font-weight: 900;
    }
    .stat-block h4 {
        font-family: 'Modesto Condensed', 'Libre Baskerville', 'Lora', 'Calisto MT', serif;
        font-size: 1.2em;
        color: #922610;
        margin: 1em 0 0.5em;
        font-variant: small-caps;
        font-weight: bold;
        border-bottom: 1px solid #922610;
    }
    .stat-block h5 {
        font-size: 1em;
        color: #922610;
        margin: 1em 0 0.2em;
        font-weight: bold;
    }
    .stat-block .tags {
        font-style: italic;
        color: #922610;
    }
    .property-block {
        margin-top: 0.3em;
        margin-bottom: 0.9em;
        line-height: 1.5;
        color: #222; /* Couleur de texte pour les blocs de propriétés */
    }
    .property-block p {
        margin: 0.2em 0;
        color: #222; /* Couleur de texte pour les paragraphes */
    }
    </style>
    """

    return nettoyer(style + potion), titre


def export_potion(potion, titre):
    nom_fichier = f"potion_images/{titre.replace(' ', '_')}.png"
    imgkit.from_string(
        potion,
        nom_fichier,
        options={"format": "png", "transparent": "", "quiet": ""},
    )
