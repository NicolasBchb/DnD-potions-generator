# 🧙‍♂️ Générateur de Potion D&D

Un générateur de potions pour Donjons & Dragons qui crée des descriptions détaillées et des images de potions aléatoires ou personnalisées.

## 🌟 Fonctionnalités

- Génération aléatoire de potions
- Personnalisation complète des potions
- Export en image
- Interface utilisateur intuitive
- Deux modes de génération de titres (Procédural / IA)

## 🚀 Installation

### Avec Docker

```bash
# Construire l'image
docker build -t potion-generator .

# Lancer le conteneur
docker run -p 8501:8501 potion-generator
```

### Installation locale

1. Cloner le dépôt
```bash
git clone https://github.com/NicolasBchb/generateur-potion-dnd.git
cd generateur-potion-dnd
```

2. Installer les dépendances
```bash
pip install -r requirements.txt
```

3. Créer un fichier `.env` avec les variables d'environnement suivantes :
```bash
OPENAI_API_KEY=votre_clé_api_openai
```

4. Lancer l'application
```bash
streamlit run streamlit_app.py
```

## 🎮 Utilisation

1. Accédez à l'application via votre navigateur : `http://localhost:8501`
2. Entrez le code PIN dans la barre latérale
3. Choisissez votre mode :
   - **Génération** : Création aléatoire de potions
   - **Sélection** : Personnalisation complète des potions

### Mode Génération
- Choisissez le nombre de potions à générer (1-10)
- Sélectionnez le type de titre (Procédural/AI)
- Cliquez sur "Générer une potion"

### Mode Sélection
- Personnalisez chaque aspect de votre potion :
  - Type de potion
  - Conteneur
  - Apparence
  - Texture
  - Goût et odeur
  - Effets (principaux et secondaires)
  - Intensité et toxicité
  - Caractéristiques spéciales

## 🛠️ Dépendances

- Python 3.10+
- Streamlit
- wkhtmltopdf
- Autres dépendances listées dans `requirements.txt`

## 📝 Notes

- Le code PIN est nécessaire pour accéder aux fonctionnalités
- Les images générées sont stockées dans le dossier `potion_images/`
- L'application utilise wkhtmltopdf pour la génération d'images

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
