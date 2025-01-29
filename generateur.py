import random
import re
import json

import dotenv
from openai import OpenAI

import imgkit

dotenv.load_dotenv()

TABLES = {
    "titres": json.load(open("tables/titres.json")),
    "conteneurs": json.load(open("tables/conteneurs.json")),
    "apparences_principales": json.load(open("tables/apparences_principales.json")),
    "apparences_avec": json.load(open("tables/apparences_avec.json")),
    "textures": json.load(open("tables/textures.json")),
    "gouts_odeurs": json.load(open("tables/gouts_odeurs.json")),
    "etiquettes": json.load(open("tables/etiquettes.json")),
    "effets_principaux": json.load(open("tables/effets_principaux.json")),
    "effets_secondaires": json.load(open("tables/effets_secondaires.json")),
    "intensite": [
        ("", "Effet de puissance normale"),
        ("Puissant", "Double effet"),
        ("Légendaire", "Triple effet"),
    ],
    "toxicite": [
        ("", "Sans effet secondaire."),
        ("Périmé", "Effet secondaire classique."),
        ("Frelaté", "Effet secondaire double."),
        ("Maudit", "Effet secondaire triple."),
    ],
    "special": [
        (
            "",
            "Pas d'effet spécial",
        ),
        (
            "Fulgurant",
            "L'effet ne dure qu'un instant, mais son intensité est décuplée.",
        ),
        (
            "A retardement",
            "L'effet est retardé de 1d6 rounds en combat ou 1d20 minutes en dehors.",
        ),
        (
            "Éternel",
            "L'effet est permanent. Un sort 'Délivrance des malédictions' peut le supprimer.",
        ),
    ],
}

genres_noms = {
    "Potion": "f",
    "Concoction": "f",
    "Fiole": "f",
    "Préparation": "f",
    "Élixir": "m",
    "Breuvage": "m",
    "Philtre": "m",
    "Tonique": "m",
    "Ichor": "m",
    "Jus": "m",
}


def accorder_intensite(nom, intensite):
    if not intensite:  # Si intensite est vide
        return ""

    genre = genres_noms.get(nom, "m")  # Par défaut masculin si nom inconnu

    if genre == "f":
        if intensite == "Puissant":
            return "Puissante"
        elif intensite == "Légendaire":
            return "Légendaire"  # Déjà invariable
    return intensite


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
    if intensite_name == "Puissant":
        nb_effets = 2
    elif intensite_name == "Légendaire":
        nb_effets = 3
    effets_principaux_list = random.sample(TABLES["effets_principaux"], nb_effets)

    # Générer le nombre approprié d'effets secondaires
    nb_effets_secondaires = 0
    if toxicite_name == "Périmé":
        nb_effets_secondaires = 1
    elif toxicite_name == "Frelaté":
        nb_effets_secondaires = 2
    elif toxicite_name == "Maudit":
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
    # Accorder l'intensité avec le nom
    intensite_accordee = accorder_intensite(
        potion_variables["nom"], potion_variables["intensite_name"]
    )

    # Construire le titre avec tous les effets principaux

    effets_list = [effet.split(".")[0] for effet in potion_variables["effets_principaux"]]
    if len(effets_list) == 1:
        effets_noms = effets_list[0]
    elif len(effets_list) == 2:
        effets_noms = f"{effets_list[0]} et {effets_list[1]}"
    else:
        effets_noms = f"{', '.join(effets_list[:-1])} et {effets_list[-1]}"

    return f"{potion_variables['nom']} {intensite_accordee} de {effets_noms} {potion_variables['special_name']} {potion_variables['toxicite_name']}".capitalize()


def titre_ai(potion_variables):
    potion_description = {
        "nom": titre_procedural(potion_variables),
        "description": f"{potion_variables['conteneur']} contient un liquide {potion_variables['apparence_principale'].lower()} {potion_variables['texture'].lower()} avec {potion_variables['apparence_avec'].lower()}. Dessus figure {potion_variables['etiquette'].lower()}. Son odeur rappelle {potion_variables['odeur'].lower()} et son goût évoque {potion_variables['gout'].lower()}.",
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
                "content": "Tu es un générateur de nom de potion DnD. A partir des caractéristiques de la potion fournies, tu dois générer un nom de potion évocateur et métaphorique, sans justification ni formatage.",
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
    <p>{potion_variables['conteneur']} contient un liquide {potion_variables['apparence_principale'].lower()} {potion_variables['texture'].lower()} avec {potion_variables['apparence_avec'].lower()}.</p>
    <p>Dessus figure {potion_variables['etiquette'].lower()}.</p>
    <p>Son odeur rappelle {potion_variables['odeur'].lower()} mais son goût évoque {potion_variables['gout'].lower()}.</p>
</div>"""

    effets_principaux = """<div class="effets-principaux">
    <h4>Effets principaux</h4>
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
    <h4>Effets secondaires</h4>
    <div class="property-block">"""

    for effet in potion_variables["effets_secondaires"]:
        nom = effet.split(". ")[0]
        description = effet[len(nom) + 1 :]
        effets_secondaires += f"""
        <h5>{nom}</h5>
        <p>{description}</p>"""
    effets_secondaires += "</div></div>"

    effets_speciaux = """<div class="effets-speciaux">
    <h4>Effets spéciaux</h4>
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
        background-image: url('https://www.aidedd.org/images/fond-ph.jpg');
        padding: 0.5em 2em;
        border: 1px solid #DDD;
        box-shadow: 0 0 1.5em #867453;
        margin: 2em;
        border-radius: 2px;
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
