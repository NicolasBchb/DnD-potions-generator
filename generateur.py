import random
import re
import json

import dotenv
from openai import OpenAI

import imgkit

dotenv.load_dotenv()


titres = [
    "Potion",
    "Concoction",
    "Fiole",
    "Préparation",
    "Élixir",
    "Breuvage",
    "Philtre",
    "Tonique",
    "Ichor",
    "Jus",
]

conteneurs = [
    "Une bouteille en verre lisse et conique",
    "Une bouteille en verre carrée",
    "Une gourde en cuir pas tout à fait étanche",
    "Une fiole en pierre",
    "Un thermos en métal",
    "Une seringue en verre",
    "Une petite fiole médicale",
    "Une bouteille de la taille d'un shot",
    "Une grande bouteille en métal",
    "Un cornet avec un bouchon",
    "Une bouteille en verre très ornée",
    "Une bouteille en forme de diamant",
    "Une longue bouteille à vin translucide",
    "Une bouteille de bière translucide",
    "Une pochette en cuir",
    "Un vaporisateur type inhalateur",
    "Une bouteille colorée",
    "Une fiole en os",
    "Une petite fiole en métal",
    "Une grande bouteille pour plusieurs gorgées",
]

apparences_principales = [
    "Transparent",
    "Bleu",
    "Vert",
    "Rouge",
    "Vert pâle",
    "Rose",
    "Bleu clair",
    "Blanc",
    "Noir",
    "Gris foncé",
    "Gris clair",
    "Jaune",
    "Orange",
    "Doré",
    "Orange",
    "Bronze",
    "Métallique",
    "Violet",
    "Marron",
    "Rouge foncé",
]

apparences_avec = [
    "Des éclats de couleur",
    "Des tourbillons de couleur",
    "Des bulles pétillantes",
    "Des bulles en suspension",
    "Un morceau d'os flottant dedans",
    "Des feuilles et des fleurs à l'intérieur",
    "Deux liquides qui se séparent",
    "Une lueur vive",
    "Une lueur douce",
    "Des rayures de couleur",
    "De la translucidité",
    "Une opacité trouble",
    "Du sang à l'intérieur",
    "De la terre flottant dedans",
    "Des morceaux de métal à l'intérieur",
    "Des restes de créature tuée",
    "De la vapeur qui s'en dégage",
    "Un visage dans le liquide",
    "Un liquide en mouvement constant",
    "Une chaleur constante",
]

textures = [
    "Épais et boueux",
    "Fin et aqueux",
    "Aéré et pétillant",
    "Visqueux",
    "Presque solide",
    "Huileux",
    "Grumeleux",
    "Granuleux",
    "Laiteux",
    "Presque gazeux",
]

gouts_odeurs = [
    "Rien du tout",
    "Le soufre",
    "L'air frais",
    "Les cookies fraîchement cuits",
    "Les fleurs",
    "La viande pourrie",
    "Les œufs",
    "Les œufs pourris",
    "Le pain frais",
    "Le sang",
    "Chez soi",
    "Le vomit",
    "L'ail",
    "Le fruit",
    "Le chocolat",
    "La bière",
    "La fumée",
    "Le bois",
    "La mort",
    "L'orc",
    "Le chien mouillé",
    "Le gobelin mouillé",
    "Le parfum",
    "Le parfum bon marché",
    "Le musc",
    "Les déchets",
    "Le sable",
    "La forêt",
    "Les noix",
    "L'acide",
    "Les épices",
    "Mentholé",
    "Les produits chimiques",
    "La terre",
    "Quelque chose de mauvais mais amélioré pour avoir meilleur goût",
    "L'alcool",
    "Le sucre",
    "Une grotte humide",
    "Étrange",
    "Indescriptible mais agréable",
    "Indescriptible mais horrible",
    "La pluie",
    "Médical",
    "Le bacon",
    "Le café",
    "L'herbe coupée",
    "La vanille",
    "La mer",
    "La viande rôtie",
    "Festif",
    "La lavande",
    "Le lilas et les groseilles",
    "Un bébé frais",
    "Une nouvelle voiture",
    "Les agrumes",
    "Le cuir",
    "Le métal",
    "Une forge",
    "Le gâteau frais",
    "La peinture",
    "Le vin",
    "Le cirage",
    "Le fromage",
    "Le poisson",
    "Le compost",
    "Les égouts",
    "Les pommes",
    "Les huiles sacrées",
    "L'huile de massage",
    "Un bordel",
    "Les vieux fruits",
    "Les roses",
    "Quelque chose qui évoque des souvenirs",
    "Le pain d'épice",
    "La cannelle",
    "Les bonbons",
    "Les vapeurs",
    "L'écorce",
    "Le poulet",
    "Le bœuf",
    "La chair humaine",
    "La poudre à canon",
    "Une tempête",
    "Le succès",
    "L'or",
    "La mayonnaise",
    "Le barbecue",
    "Le sel",
    "Le poivre",
    "Les épices aromatiques",
    "Le punch aux fruits",
    "L'eau",
    "L'eau fraîche",
    "L'eau stagnante",
    "La boue",
    "Une couleur",
    "La musique",
    "La fin du monde",
    "Magiquement la pire chose pour vous",
    "Magiquement la chose la plus désirable pour vous",
]

etiquettes = [
    "Son nom et son titre en lettres majuscules",
    "Sa description en elfique orné",
    "Sa description en elfique avec une histoire mythique pertinente",
    "Sa description en nain",
    "Des runes naines",
    "Sa description en gnome",
    "Des diagrammes gnomes pour son utilisation",
    'Les mots "À UTILISER UNIQUEMENT EN CAS D\'URGENCE" griffonnés dessus',
    "Une étiquette imprimée indiquant que la société n'est pas responsable des effets secondaires",
    "Une étiquette imprimée indiquant que c'est une nouvelle saveur",
    "Une très petite police décrivant en détail comment la potion a été faite, environ 1000 mots",
    "Son nom en lettres majuscules en géant",
    "L'étiquette est griffonnée",
    "L'étiquette est effacée et illisible",
    "L'étiquette semble manquante",
    "Sa description et un fait aléatoire",
    "Sa description et un petit compliment pour égayer votre journée",
    "Sa description et une blague",
    "Sa description en infernal",
    "Sa description dans une langue ancienne",
    "Tout en symboles",
    "Tout en symboles en relief pour les aveugles",
    "Sa description en langues élémentaires",
    "Son nom et sa saveur",
    "Son nom avec un avertissement sur les effets secondaires",
    "Son nom et son prix recommandé",
    "Des empreintes sanglantes partout",
    "Le nom gravé sur le contenant",
    "Son nom brillant avec une magie mineure",
    "Une mascotte cartoon",
    "Un avertissement sur une ancienne malédiction",
    "Son nom et sa description en encre invisible",
    "Sa description en draconique",
    "Plusieurs noms et descriptions différents superposés",
    "Le nom d'une potion complètement différente de ce qu'elle fait",
    "Un titre décrivant exactement le contraire",
    "Une garantie de remboursement",
    "Un coupon pour une potion gratuite",
    "Un visage vivant qui regarde autour",
    "Son nom et la recette pour d'autres alchimistes",
    "Une lettre d'amour sincère pour quelqu'un",
    "Une lettre de haine sincère pour quelqu'un",
    "Le nom d'une personne. La potion ne fonctionnera pas à moins qu'on ne lui demande par son nom",
    "Une étrange prophétie",
    "Un petit dessin",
    'Une note disant "NE PAS BOIRE"',
    "Une note passive-agressive sur les gens qui boivent des potions qui ne leur appartiennent pas",
    "Des lettres brillamment lumineuses",
    "Une chanson très silencieuse qui joue jusqu'à ce que la bouteille soit vide",
    "Des designs ornés et magnifiques",
    "Des designs très pratiques",
    "Des symboles sacrés",
    "Des symboles profanes",
    "Des symboles féeriques et une écriture sylvestre",
    "Une énigme, le bouchon ne s'ouvrant pas à moins que l'énigme ne soit résolue",
    "Une note disant qu'elle est conçue pour les bébés",
    "Une note disant qu'elle ne doit pas être bue par les moins de 18 ans",
    "Une note disant que c'est de la contrebande illégale confisquée",
    "Une note disant que l'alchimiste pense que c'est son plus grand travail",
    "Une note disant que l'alchimiste regrette de l'avoir créée",
    "Une note disant qu'elle n'aurait jamais dû être faite et des taches de sang partout sur la bouteille",
    'Une note disant "Vous êtes surveillé". Quand la personne vérifie, elle dit "Je plaisante"',
    "Sa description en druidique",
    "Sa description en orc",
    "Sa description en gobelin",
    "Sa description en halfelin",
    "Sa description en céleste",
    "Sa description en commun des profondeurs",
    "Sa description en langage des abysses",
    "Sa description en symboles arcaniques étranges",
    "Une carte de l'endroit où la potion a été fabriquée",
    "Un petit puzzle pour enfants",
    "Une liste d'ingrédients sous leurs formes chimiques",
    "Une liste d'effets secondaires aussi longue que la bouteille",
    "Une croix rouge",
    "Un visage triste",
    "Un visage en colère",
    "Un visage heureux",
    "Un symbole de guérison",
    "Un nom de potion avec un jeu de mots ringard",
    "Des vignes qui poussent dessus",
    "Des fleurs qui poussent dessus",
    "Des cristaux qui poussent dessus",
    "De la roche qui pousse dessus",
    "Des symboles chamaniques et des copeaux",
    "Pas de mots, juste une seule couleur",
    "Des dommages causés par l'eau, mais une étiquette encore lisible",
    "Une étiquette comme si c'était un cadeau",
    "Une étiquette indiquant le nombre de calories",
    "Un avertissement sur l'abus de potions et de ne prendre qu'avec modération",
    "Une étiquette avec des avertissements et des effets secondaires tous griffonnés",
    "Une étiquette qui ne montre que les effets secondaires",
    "Un numéro mystérieux",
    "Un nom de code",
    "Quelques lettres sans rapport",
    "Le nom d'un des membres du groupe",
    "Le nom du méchant",
    "Des insectes rampant dessus",
    "Recouverte de quelque chose d'indicible",
    "Recouverte de paillettes. Ça se répand partout",
]

effets_principaux = [
    "Soin. Régénère instantanément des points de vie lorsqu'elle est bue. Régénère 2d6+4 PV.",
    "Vigueur. Donne des points de vie temporaires lorsqu'elle est bue. Donne 1d10 PV temporaires pendant 1 heure.",
    "Vitalité. Régénère lentement des points de vie sur une période de quelques heures. Régénère 1 PV par minute pendant 1 heure.",
    "Puissance. Donne un bonus aux jets d'attaque après avoir été bue. +2 aux jets d'attaque pendant 10 minutes.",
    "Courage. Immunise contre la peur et donne une inspiration temporaire. Immunité à la peur et avantage sur les jets de sauvegarde de Sagesse pendant 1 heure.",
    "Force de géant. Donne une force bien supérieure à l'utilisateur. La Force devient 25 pendant 1 minute.",
    "Résistance à la flamme. Donne une résistance aux dégâts de feu. Résistance aux dégâts de feu pendant 1 heure.",
    "Résistance au froid. Donne une résistance aux dégâts de froid. Résistance aux dégâts de froid pendant 1 heure.",
    "Résistance nécrotique. Donne une résistance aux dégâts nécrotiques. Résistance aux dégâts nécrotiques pendant 1 heure.",
    "Résistance radiante. Donne une résistance aux dégâts radiants. Résistance aux dégâts radiants pendant 1 heure.",
    "Peau de pierre. Donne une résistance aux dégâts physiques. Résistance aux dégâts contondants, perforants et tranchants pendant 10 minutes.",
    "Résistance à l'acide. Donne une résistance aux dégâts d'acide. Résistance aux dégâts d'acide pendant 1 heure.",
    "Résistance à la foudre. Donne une résistance aux dégâts de foudre. Résistance aux dégâts de foudre pendant 1 heure.",
    "Charme de succube. Rend l'utilisateur irrésistible aux personnes à proximité. Les créatures à 9 mètres doivent réussir un jet de sauvegarde de Sagesse (DD 15) ou être charmées pendant 1 heure.",
    "Bouclier. Donne à l'utilisateur un bouclier magique d'énergie. +2 à la CA pendant 1 minute.",
    "Souffle de flamme. Donne à l'utilisateur un souffle de feu pendant un court moment. Souffle de feu (4d6 dégâts, cône de 4,5 mètres) pendant 1 minute.",
    "Croissance. Fait doubler la taille de l'utilisateur. La taille double et les dégâts des attaques augmentent de 1d4 pendant 10 minutes.",
    "Rétrécissement. Réduit la taille de l'utilisateur de moitié. La taille est réduite de moitié et la CA augmente de +2 pendant 10 minutes.",
    "Compréhension. Permet à l'utilisateur de comprendre toutes les langues. Comprend toutes les langues pendant 1 heure.",
    "Fertilité. Rend l'utilisateur très fertile, presque certain de concevoir un enfant sous son effet ! Fertilité maximale pendant 24 heures.",
    "Intimidation. Donne à l'utilisateur une voix puissante qui terrifie ceux qui l'entourent. Les créatures à 9 mètres doivent réussir un jet de sauvegarde de Charisme (DD 15) ou être effrayées pendant 1 minute.",
    "Chance. Donne à l'utilisateur un boost temporaire de chance. Avantage sur les jets de dés pendant 1 heure.",
    "Mana. Donne à l'utilisateur plus de puissance magique pour lancer des sorts. Récupère 1d4 emplacements de sorts.",
    "Arcanes. Donne à l'utilisateur des sorts plus puissants. Les sorts infligent +2 dégâts pendant 1 heure.",
    "Forme animale. Transforme l'utilisateur en un animal aléatoire. Transformation en animal (CR 1 ou moins) pendant 1 heure.",
    "Rêves. Plonge l'utilisateur dans un monde de rêves hallucinatoires de son rêve parfait. Hallucinations pendant 1 heure.",
    "Cauchemars. Plonge l'utilisateur dans un monde de cauchemars hallucinatoires de ses pires cauchemars. Effrayé et désorienté pendant 1 heure.",
    "Endurance. Donne à l'utilisateur plus d'endurance et de constitution. +2 à la Constitution pendant 1 heure.",
    "Pieds agiles. Donne à l'utilisateur plus de vitesse. Vitesse augmentée de 3 mètres pendant 1 heure.",
    "Connaissance. Augmente temporairement l'intelligence de l'utilisateur. +2 à l'Intelligence pendant 1 heure.",
    "Barde. Augmente temporairement le Charisme de l'utilisateur. +2 au Charisme pendant 1 heure.",
    "Déguisement. Change la forme de l'utilisateur en un déguisement de n'importe quelle race et apparence. Transformation en une autre apparence pendant 1 heure.",
    "Festin. Supprime toute faim et soif de la cible. Nourrit et hydrate complètement pendant 24 heures.",
    "Jeunesse. Rend l'utilisateur plus jeune de quelques années. Réduit l'âge de 1d10 années pendant 24 heures.",
    "Vieillesse. Vieillit l'utilisateur de quelques années. Augmente l'âge de 1d10 années pendant 24 heures.",
    "Fournaise. Fait rayonner l'utilisateur avec une aura de dégâts. Aura de 1d6 dégâts de feu dans un rayon de 1,5 mètre pendant 1 minute.",
    "Vue d'aigle. Donne à l'utilisateur une vision perçante et un bonus à la perception. +5 à la Perception et vision dans le noir pendant 1 heure.",
    "Santé. Guérit toutes les maladies et maladies. Guérit toutes les maladies et conditions.",
    "Invulnérabilité. Gèle l'utilisateur dans une stase qui le rend immunisé aux dégâts mais il ne peut pas bouger ou agir. Immunité aux dégâts mais paralysé pendant 1 minute.",
    "Énigme résolue. Donne à l'utilisateur la solution à une seule énigme. Résout une énigme spécifique.",
    "Apparence horrifiante. Rend l'utilisateur plus laid pendant un moment. -2 au Charisme pendant 1 heure.",
    "Apparence magnifique. Rend l'utilisateur plus attirant pendant un moment. +2 au Charisme pendant 1 heure.",
    "Maîtrise de l'épée. Rend l'utilisateur plus efficace et polyvalent avec une lame. +2 aux jets d'attaque avec des armes de mêlée pendant 1 heure.",
    "Maîtrise de l'arc. Rend l'utilisateur plus efficace avec un arc ou une arme à distance. +2 aux jets d'attaque avec des armes à distance pendant 1 heure.",
    "Souffle de nymphe. Permet à l'utilisateur de respirer sous l'eau. Respiration aquatique pendant 1 heure.",
    "Midas. Transforme les objets en or. Transforme un objet en or (jusqu'à 30 cm de diamètre) pendant 1 heure.",
    "Berserker. Fait entrer l'utilisateur dans une rage de grande force. Avantage sur les jets de force et +2 aux dégâts pendant 1 minute.",
    "Haine absolue. Donne à l'utilisateur des bonus contre un type d'ennemi particulier. +2 aux jets d'attaque et de dégâts contre un type d'ennemi spécifique pendant 1 heure.",
    "Oracle. Permet à l'utilisateur de deviner l'avenir. Peut poser une question sur l'avenir et obtenir une réponse vague.",
    "Sangsue démoniaque. Soigne une partie des dégâts infligés par l'utilisateur. Soigne 1d6 PV pour chaque 10 dégâts infligés pendant 1 heure.",
    "Nature féerique. Permet à l'utilisateur de devenir un avec les animaux et la nature environnante. Communication avec les animaux et avantage aux jets de Nature pendant 1 heure.",
    "Sans trace. Rend l'utilisateur très difficile à suivre. Avantage aux jets de Discrétion et pas de traces physiques pendant 1 heure.",
    "Grâce. Améliore les compétences d'acrobatie de l'utilisateur. +5 aux tests d'Acrobatie pendant 1 heure.",
    "Escalade de gobelin. Donne à l'utilisateur un bonus à l'escalade. +5 aux tests d'Escalade pendant 1 heure.",
    "Mort apparente. Rend l'utilisateur complètement mort à toute magie. Apparaît mort aux détections magiques pendant 1 heure.",
    "Trèfle à une feuille. Donne à l'utilisateur une malchance. Désavantage sur tous les jets de dés pendant 1 heure.",
    "Possession. Permet à l'utilisateur de prendre le contrôle d'une créature proche, son corps devenant comateux. Contrôle une créature pendant 1 minute (jet de sauvegarde de Sagesse DD 15).",
    "Veille du hibou. Rend l'utilisateur sans besoin de sommeil pendant un moment. Pas besoin de dormir pendant 24 heures.",
    "Vol du faucon. Permet à l'utilisateur de voler. Vol pendant 10 minutes.",
    "Paix. Rend l'utilisateur très calme et incapable de nuire aux autres. Incapacité d'attaquer ou de nuire pendant 1 heure.",
    "Réjuvénation. Guérit une seule cicatrice ou blessure grave sur l'utilisateur, comme un bras manquant. Guérit une blessure permanente.",
    "Vérité du sphinx. Force l'utilisateur à dire la vérité. Incapacité de mentir pendant 1 heure.",
    "Langue de serpent. Force l'utilisateur à ne pouvoir que mentir. Incapacité de dire la vérité pendant 1 heure.",
    "Navigation. Rend l'utilisateur incapable de se perdre et lui permet de trouver ce dont il a besoin. Impossible de se perdre et trouve le chemin le plus court pendant 1 heure.",
    "Griffes d'horreur. Les mains de l'utilisateur deviennent des lames tranchantes. Les mains infligent 1d8 dégâts tranchants pendant 10 minutes.",
    "Schadenfreude. Fait que les ennemis subissent des dégâts lorsqu'ils en infligent à l'utilisateur. Les ennemis subissent la moitié des dégâts infligés à l'utilisateur pendant 1 minute.",
    "Invisibilité. Rend l'utilisateur invisible. Invisibilité pendant 10 minutes.",
    "Magie sauvage. Accède à la magie sauvage, provoquant un effet absolument aléatoire. Effet aléatoire de la table de magie sauvage.",
    "Renommée. Rend l'utilisateur plus célèbre. +2 au Charisme dans les interactions sociales pendant 24 heures.",
    "Marche de chèvre. Rend l'utilisateur immunisé aux fatigues des longs voyages et aux intempéries. Immunité à la fatigue due aux voyages et aux conditions météorologiques pendant 24 heures.",
    "Ténacité de gargouille. Augmente la constitution de l'utilisateur. +2 à la Constitution pendant 1 heure.",
    "Horloge atomique. Permet à l'utilisateur de connaître l'heure et la date exactes. Connaît l'heure et la date exactes en permanence.",
    "Transmutation. Permet à l'utilisateur de changer les propriétés de quelque chose. Transforme un objet en un autre objet de même taille pendant 1 heure.",
    "Peau de fer. Transforme la peau de l'utilisateur en métal, lui conférant de nombreuses résistances. Résistance aux dégâts physiques et +2 à la CA pendant 10 minutes.",
    "Changement de sexe. Change le sexe de l'utilisateur. Changement de sexe pendant 24 heures.",
    "Changement de race. Change la race de l'utilisateur. Changement de race pendant 24 heures.",
    "Souffle musical. Fait que l'utilisateur dit tout en chanson, et une musique féerique l'accompagne dans l'air. Parle en chanson et attire l'attention pendant 1 heure.",
    "Compréhension totale. Rend l'utilisateur très intime avec une chose précise. Aléatoire ou choisi. Connaissance approfondie d'un sujet spécifique pendant 1 heure.",
    "Forme divisée. L'utilisateur se transforme en deux ou trois petites versions de lui-même et les contrôle toutes. Divise en 2 ou 3 versions miniatures pendant 10 minutes.",
    "Saveur. Rend tout délicieux ! Tout ce qui est mangé ou bu a un goût incroyable pendant 1 heure.",
    "Scintillement. Nettoie instantanément l'utilisateur et son équipement, les rendant aussi beaux que possible. Nettoie et embellit l'utilisateur et son équipement pendant 1 heure.",
    "Amour. Fait tomber l'utilisateur et quelqu'un d'autre amoureux. Charmé par une créature spécifique pendant 1 heure.",
    "Poison. Empoisonne l'utilisateur, l'affaiblissant. Empoisonné pendant 1 heure (désavantage aux jets d'attaque et de sauvegarde).",
    "Renaissance. Ressuscite l'utilisateur s'il meurt peu après avoir bu. Ressuscite avec 1 PV si mort dans les 10 minutes.",
    "Forme élémentaire. Transforme l'utilisateur en une forme élémentaire correspondant à sa personnalité. Transformation en élémentaire (feu, eau, terre, air) pendant 10 minutes.",
    "Forme véritable. Transforme l'utilisateur en une créature familière similaire à sa personnalité. Transformation en familier (chat, chien, oiseau, etc.) pendant 1 heure.",
    "Toucher divin. Donne à l'utilisateur une connexion sacrée à sa divinité ou à une entité démoniaque. Avantage sur les jets liés à la religion et aux soins pendant 1d6 heures.",
    "Antidépresseur. Améliore l'humeur de l'utilisateur et réduit les effets de peur ou de tristesse. Immunité à la peur et au désespoir pendant 1 heure.",
    "Forme fantomatique. Rend l'utilisateur intangible et capable de traverser les objets solides. Intangibilité pendant 1 minute.",
    "Compétence d'artisan. Donne à l'utilisateur une grande habileté dans un art spécifique temporairement. Compétence experte dans un art ou artisanat pendant 1 heure.",
    "Forme divine. Améliore toutes les statistiques de l'utilisateur temporairement. +4 à toutes les caractéristiques pendant 10 minutes.",
    "Armes bénies. Les armes de l'utilisateur infligent des dégâts supplémentaires. +1d8 dégâts radieux avec les armes pendant 10 minutes.",
    "Euphorie. Donne à l'utilisateur un sentiment de bonheur extrême et des visions hallucinatoires. Avantage sur les jets de Charisme, désavantage sur la Perception, pendant 10 minutes.",
    "Garde du corps. Crée un garde du corps spectral temporaire obéissant aux ordres de l'utilisateur. Invoque un garde spectral avec 20 PV pendant 10 minutes.",
    "Babelfish. Permet à l'utilisateur de parler n'importe quelle langue, mais sans la comprendre. Capacité de parler toutes les langues pendant 1 heure.",
    "Préservation. Empêche tout ce sur quoi la potion est versée de pourrir ou se dégrader. Conserve un objet ou de la nourriture pendant 1d6 jours.",
    "Peur. Rend l'utilisateur terrifié. L'utilisateur est effrayé pendant 1 minute (test de sauvegarde de Sagesse pour résister).",
    "Vision nocturne. Permet de voir dans l'obscurité comme en plein jour. Vision dans l'obscurité jusqu'à 60 pieds pendant 8 heures.",
    "Pistage. Permet à l'utilisateur de traquer un ennemi avec précision. Avantage sur les jets de Survie pour suivre des traces pendant 1 heure.",
    "Panacée. Guérit tous les effets de statut affectant l'utilisateur. Supprime tous les états négatifs (poison, paralysie, maladie, etc.).",
]

effets_secondaires = [
    "Endort l'utilisateur pendant 1d4 heures.",
    "Pousse rapide de poils sur tout le corps pendant 1d6 heures.",
    "Saignement des yeux pendant 1d4 rounds.",
    "Hallucinations vives pendant 1d10 minutes.",
    "Flashbacks de votre propre mort éventuelle.",
    "La peau se fissure et apparaît déformée pendant 1d4 heures.",
    "Des taches apparaissent sur la peau pendant 1d6 jours.",
    "Diarrhée pendant 1d4 heures.",
    "Vomissements pendant 1d4 rounds.",
    "Vision floue pendant 1d6 rounds.",
    "Cécité pendant 1d4 rounds.",
    "Surdité pendant 1d4 rounds.",
    "Mutisme pendant 1d6 rounds.",
    "Perte de santé due à un saignement rapide (1d6 dégâts par round pendant 1d4 rounds).",
    "Un accent horrible soudain pendant 1d6 heures.",
    "Une envie irrésistible de danser pendant 1d4 rounds.",
    "Entendre des démons pendant 1d6 rounds.",
    "Perte d'équilibre pendant 1d4 rounds.",
    "Tout a un goût de terre pendant 1d6 heures.",
    "Salivation excessive pendant 1d4 rounds.",
    "Perte d'intelligence (-1d4 à l'INT) pendant 1d6 heures.",
    "Perte de force (-1d4 à la FOR) pendant 1d6 heures.",
    "Perte de vitesse (-1d4 à la DEX) pendant 1d6 heures.",
    "Perte de charisme (-1d4 au CHA) pendant 1d6 heures.",
    "Bonheur authentique pendant 1d6 heures.",
    "Faim extrême.",
    "Soif extrême.",
    "Difficultés à respirer pendant 1d4 rounds.",
    "Moustache soudaine pendant 1d6 heures.",
    "Empoisonnement (1d6 dégâts de poison par round pendant 1d4 rounds).",
    "Pétrification pendant 1d4 rounds.",
    "Étourdissement pendant 1d4 rounds.",
    "Immobilisation pendant 1d4 rounds.",
    "Libido augmentée pendant 1d6 heures.",
    "Agitation nerveuse pendant 1d4 rounds.",
    "Démangeaisons pendant 1d6 heures.",
    "Éruptions cutanées pendant 1d6 jours.",
    "Attire les ours pendant 1d6 heures.",
    "Recouvert de boue magiquement pendant 1d4 heures.",
    "Odeur horrible pendant 1d6 heures.",
    "Calvitie soudaine.",
    "Gonflement du corps pendant 1d4 heures.",
    "Perte d'un objet aléatoire.",
    "Malédiction aléatoire pendant 1d6 jours.",
    "Dégâts (1d6 dégâts immédiats).",
    "Faiblesse à un type de dégâts magiques pendant 1d6 heures.",
    "Faiblesse aux dégâts physiques pendant 1d6 heures.",
    "Sentiments de culpabilité pendant 1d6 heures.",
    "Sentiments d'anxiété pendant 1d6 heures.",
    "Sentiments de honte pendant 1d6 heures.",
    "Éternuements incontrôlables pendant 1d4 rounds.",
    "Pleurs incontrôlables pendant 1d4 rounds.",
    "Besoin de chanter de la musique héroïque pendant 1d6 rounds.",
    "Envie de faire des câlins pendant 1d6 rounds.",
    "Kleptomanie pendant 1d6 heures.",
    "Rots incontrôlables pendant 1d4 rounds.",
    "Perte d'odorat pendant 1d6 heures.",
    "Insomnie pendant 1d6 heures.",
    "Paranoïa pendant 1d6 heures.",
    "Malchance (-1d4 aux jets de dés) pendant 1d6 heures.",
    "Invocation d'imps qui veulent vous tuer (1d4 imps).",
    "Invocation d'abeilles en colère (1d6 abeilles).",
    "Peur de quelque chose pendant 1d6 heures.",
    "Folie temporaire pendant 1d6 rounds.",
    "Relaxation totale pendant 1d6 heures.",
    "Appréciation accrue des couleurs et des sons pendant 1d6 heures.",
    "Trip intense pendant 1d6 rounds.",
    "Désir douloureux pendant 1d6 rounds.",
    "Étourdissement pendant 1d4 rounds.",
    "Confiance en soi augmentée pendant 1d6 heures.",
    "Imprudence pendant 1d6 heures.",
    "Rage incontrôlable pendant 1d6 rounds.",
    "Tristesse intense pendant 1d6 heures.",
    "Vertiges pendant 1d4 rounds.",
    "Douleur intense (1d6 dégâts).",
    "Possession légère pendant 1d6 rounds.",
    "Réaction allergique à votre nourriture préférée pendant 1d6 heures.",
    "Croyance forte que vous êtes quelqu'un d'autre pendant 1d6 heures.",
    "Dette soudaine (perte de 1d6 x 10 pièces d'or).",
    "Grincheux pendant 1d6 heures.",
    "Spasmes musculaires pendant 1d4 rounds.",
    "Sensation de ballonnement pendant 1d6 heures.",
    "Rhume pendant 1d6 heures.",
    "Fièvre pendant 1d6 heures.",
    "Devenir étrangement léger (réduction de poids de 50%) pendant 1d6 heures.",
    "Faiblesse générale (-1d4 à toutes les caractéristiques) pendant 1d6 heures.",
    "Envie de combattre pendant 1d6 rounds.",
    "Besoin de se faire des amis pendant 1d6 heures.",
    "Nausées pendant 1d4 rounds.",
    "Sautes d'humeur pendant 1d6 heures.",
    "Addiction à la potion pendant 1d6 jours.",
    "Besoin impérieux de boire de l'alcool pendant 1d6 heures.",
    "Ivresse pendant 1d6 heures.",
    "Toux incontrôlable pendant 1d4 rounds.",
    "Bavardage incontrôlable pendant 1d6 rounds.",
    "Douleurs légères (1d4 dégâts).",
    "Mauvais goût dans la bouche pendant 1d6 heures.",
    "Vertiges pendant 1d4 rounds.",
    "Rires incontrôlables pendant 1d6 rounds.",
]

intensite = [
    ("", "Effet de puissance normale"),
    ("Puissant", "Double effet"),
    ("Légendaire", "Triple effet"),
]

toxicite = [
    ("", "Sans effet secondaire."),
    ("Périmé", "Effet secondaire classique."),
    ("Frelaté", "Effet secondaire double."),
    ("Maudit", "Effet secondaire triple."),
]

special = [
    ("", "Pas d'effet spécial"),
    ("Fulgurant", "L'effet ne dure qu'un instant, mais son intensité est décuplée."),
    (
        "A retardement",
        "L'effet est retardé de 1d6 rounds en combat ou 1d20 minutes en dehors.",
    ),
    (
        "Éternel",
        "L'effet est permanent. Un sort 'Délivrance des malédictions' peut le supprimer.",
    ),
]

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
        "nom": random.choice(titres),
        "conteneur": random.choice(conteneurs),
        "apparence_principale": random.choice(apparences_principales),
        "apparence_avec": random.choice(apparences_avec),
        "texture": random.choice(textures),
        "gout": random.choice(gouts_odeurs),
        "odeur": random.choice(gouts_odeurs),
        "etiquette": random.choice(etiquettes),
        "effet_principal": random.choice(effets_principaux),
    }

    intensite_name, intensite_effect = random.choices(
        intensite, weights=[60, 35, 5], k=1
    )[0]
    toxicite_name, toxicite_effect = random.choices(
        toxicite, weights=[30, 30, 15, 5], k=1
    )[0]
    special_name, special_effect = random.choices(
        special, weights=[79, 10, 10, 1], k=1
    )[0]

    # Générer le nombre approprié d'effets principaux
    nb_effets = 1
    if intensite_name == "Puissant":
        nb_effets = 2
    elif intensite_name == "Légendaire":
        nb_effets = 3
    effets_principaux_list = random.sample(effets_principaux, nb_effets)

    # Générer le nombre approprié d'effets secondaires
    nb_effets_secondaires = 0
    if toxicite_name == "Périmé":
        nb_effets_secondaires = 1
    elif toxicite_name == "Frelaté":
        nb_effets_secondaires = 2
    elif toxicite_name == "Maudit":
        nb_effets_secondaires = 3
    effets_secondaires_list = (
        random.sample(effets_secondaires, nb_effets_secondaires)
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
    effets_noms = " ".join(
        [effet.split(".")[0] for effet in potion_variables["effets_principaux"]]
    )

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


def generer_potion(type_titre="Procedural"):
    potion_variables = roll_potion()

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
    <p>Son odeur rappelle {potion_variables['odeur'].lower()} et son goût évoque {potion_variables['gout'].lower()}.</p>
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

    if potion_variables["effets_secondaires"]:
        for effet in potion_variables["effets_secondaires"]:
            effets_secondaires += f"<p>{effet.capitalize()}</p>"
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
        options={
            "format": "png",
            "transparent": "",
            "quiet": ""
        },
    )

