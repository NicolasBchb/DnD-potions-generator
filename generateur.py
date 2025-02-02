import random
import re
import json
import os
import datetime

import dotenv
from openai import OpenAI

import imgkit
from jinja2 import Environment, FileSystemLoader

dotenv.load_dotenv()


class Potion:
    def __init__(self, lang="fr"):
        self.lang = lang

        self.tables = {
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

    def roll(self):
        self.type = random.choice(self.tables["titles"])
        self.container = random.choice(self.tables["containers"])
        self.main_appearance = random.choice(self.tables["main_appearances"])
        self.with_appearance = random.choice(self.tables["with_appearances"])
        self.texture = random.choice(self.tables["textures"])
        self.taste = random.choice(self.tables["tastes_smells"])
        self.smell = random.choice(self.tables["tastes_smells"])
        self.label = random.choice(self.tables["labels"])

        self.intensity = random.choices(
            self.tables["intensities"], weights=[60, 35, 5], k=1
        )[0]
        self.toxicity = random.choices(
            self.tables["toxicities"], weights=[30, 30, 15, 5], k=1
        )[0]
        self.special = random.choices(
            self.tables["specials"], weights=[79, 10, 10, 1], k=1
        )[0]

        # Générer le nombre approprié d'effets principaux
        self.main_effects = random.sample(
            self.tables["main_effects"], self.intensity["nb_effects"]
        )

        # Générer le nombre approprié d'effets secondaires
        self.side_effects = (
            random.sample(self.tables["side_effects"], self.toxicity["nb_effects"])
            if self.toxicity["nb_effects"] > 0
            else []
        )

    def accorder(self, nom, intensite, toxicite):
        feminin = [
            "Potion",
            "Concoction",
            "Fiole",
            "Préparation",
        ]
        intensite_accordee = intensite["name"]
        toxicite_accordee = toxicite["name"]

        if nom in feminin:
            if intensite["name"] == "Puissant":
                intensite_accordee = "Puissante"

            if toxicite["name"] == "Périmé":
                toxicite_accordee = "Périmée"
            elif toxicite["name"] == "Frelaté":
                toxicite_accordee = "Frelatée"
            elif toxicite["name"] == "Maudite":
                toxicite_accordee = "Maudite"

        return intensite_accordee, toxicite_accordee

    def procedural_title(self):
        if self.lang == "fr":
            # Accorder l'intensité avec le nom
            intensite_accordee, toxicite_accordee = self.accorder(
                self.type, self.intensity, self.toxicity
            )

            # Construire le titre avec tous les effets principaux
            if len(self.main_effects) == 0:
                effets_noms = ""
            elif len(self.main_effects) == 1:
                effets_noms = self.main_effects[0]["name"]
            elif len(self.main_effects) == 2:
                effets_noms = (
                    f"{self.main_effects[0]['name']} et {self.main_effects[1]['name']}"
                )
            else:
                effets_noms = f"{self.main_effects[0]['name']}, {self.main_effects[1]['name']} et {self.main_effects[2]['name']}"

            titre = f"{self.type} {intensite_accordee} de {effets_noms} {self.special['name']} {toxicite_accordee}".capitalize()

            # Remplacer "de" par "d'" devant les voyelles et le h muet
            return re.sub(
                r"\bde (?=[aeiouyéàâäëêèïîôöùûüÿhAEIOUYÉÀÂÄËÊÈÏÎÔÖÙÛÜŸH])", "d'", titre
            ).strip()

        elif self.lang == "en":
            # Construire le titre avec tous les effets principaux
            if len(self.main_effects) == 0:
                effets_noms = ""
            elif len(self.main_effects) == 1:
                effets_noms = self.main_effects[0]["name"]
            elif len(self.main_effects) == 2:
                effets_noms = (
                    f"{self.main_effects[0]['name']} and {self.main_effects[1]['name']}"
                )
            else:
                effets_noms = f"{self.main_effects[0]['name']}, {self.main_effects[1]['name']} and {self.main_effects[2]['name']}"

            return f"{self.intensity['name'].lower()} {self.toxicity['name'].lower()} {self.special['name'].lower()} {self.type.lower()} of {effets_noms}".strip().capitalize()

    def ai_title(self):
        with open(f"l10n/{self.lang}/prompt.txt", "r") as f:
            prompt = f.read()

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "conteneur": self.container,
                            "apparence": f"{self.main_appearance} {self.texture} avec {self.with_appearance}",
                            "odeur": self.smell,
                            "gout": self.taste,
                            "effets_principaux": [
                                effect["name"] for effect in self.main_effects
                            ],
                            "effets_secondaires": [
                                effect["name"] for effect in self.side_effects
                            ],
                            "effets_speciaux": self.special["name"],
                        }
                    ),
                },
            ],
            max_tokens=50,
            temperature=0.9,
        )
        return completion.choices[0].message.content

    def design_potion(self, title_type="Procedural", export=False):
        # Format title
        if title_type == "Procedural":
            self.titre = self.procedural_title()
        elif title_type == "AI":
            self.titre = self.ai_title()
        else:
            self.titre = title_type

        # Format tags
        tags = [
            tag.capitalize()
            for tag in [
                self.intensity["name"],
                self.toxicity["name"],
                self.special["name"],
            ]
            if tag
        ]
        tags = ", ".join(tags) if tags else ""

        # Setup Jinja environment
        env = Environment(loader=FileSystemLoader(f"l10n/{self.lang}/"))
        template = env.get_template("card.html")

        # Prepare template variables
        template_vars = {
            "title": self.titre,
            "tags": tags,
            "container": self.container,
            "main_appearance": self.main_appearance.lower(),
            "texture": self.texture.lower(),
            "with_appearance": self.with_appearance.lower(),
            "label": self.label.lower(),
            "smell": self.smell.lower(),
            "taste": self.taste.lower(),
            "main_effects": self.main_effects,
            "side_effects": self.side_effects,
            "special_effect": self.special,
            "lang": self.lang,
        }

        # Render template
        self.html = template.render(**template_vars)

        if export:
            nom_fichier = f"potion_images/{self.titre.replace(' ', '_')}.png"
            imgkit.from_string(
                self.html,
                nom_fichier,
                options={"format": "png", "transparent": "", "quiet": ""},
            )

        return self.html

    def save_potion_log(self, ai):
        with open("logs/logs.csv", "a") as f:
            f.write(
                f"{datetime.datetime.now()};{self.lang};{ai};{self.titre};{self.container};{self.main_appearance};{self.with_appearance};{self.texture};{self.taste};{self.smell};{self.label};{self.intensity['name']};{self.toxicity['name']};{self.special['name']};{self.main_effects};{self.side_effects}\n"
            )


def initialize_logs():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open("logs/logs.csv", "w") as f:
        f.write(
            "date;language;ai;title;name;container;main_appearance;with_appearance;texture;taste;smell;label;intensity;toxicity;special;main_effects;side_effects\n"
        )
