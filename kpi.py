import datetime


def initialize_logs():
    with open("logs/logs.csv", "w") as f:
        f.write(
            "date; language; ai; title; name; container; main_appearance; with_appearance; texture; taste; smell; label; intensity; toxicity; special; special_effect; main_effects; side_effects\n"
        )


def log_potion(language, ai, titre, potion_data):
    with open("logs/logs.csv", "a") as f:
        f.write(
            f"{datetime.datetime.now()}; {language}; {ai}; {titre}; {potion_data['nom']}; {potion_data['conteneur']}; {potion_data['apparence_principale']}; {potion_data['apparence_avec']}; {potion_data['texture']}; {potion_data['gout']}; {potion_data['odeur']}; {potion_data['etiquette']}; {potion_data['intensite_name']}; {potion_data['toxicite_name']}; {potion_data['special_name']}; {potion_data['special_effect']}; {potion_data['effets_principaux']}; {potion_data['effets_secondaires']}\n"
        )

