# 🌱 Projet de Simulation d'Arbres et d'Animaux 🦊

Bienvenue dans ce projet qui simule la croissance d'arbres et le comportement d'animaux dans un écosystème procédural ! 🌍

## Description

Ce projet génère une carte de nutriments à l'aide de bruit de Perlin, puis y place des arbres et des animaux. Les arbres poussent, changent d'état (graine, vivant, mort) et interagissent avec leur environnement. Les animaux, quant à eux, se déplacent, tournent, consomment de la nourriture et influencent le vieillissement des arbres. 🍃

## Fonctionnalités

- **Carte de nutriments générée par Perlin Noise** : chaque pixel possède une valeur de nutriments affectant la croissance des arbres.
- **Arbres** :  
  - États possibles : `seed`, `alive`, `dead`  
  - Croissance du rayon, stockage d'énergie, vieillissement automatique  
  - Apparition aléatoire, évolution avec le temps, affichage graphique 💮
- **Animaux** :  
  - Se déplacent, tournent à gauche ou à droite  
  - Ont une faim qui augmente avec le temps  
  - Peuvent manger un arbre s'ils sont suffisamment proches, réduisant ainsi leur faim et faisant vieillir l'arbre de 2 ans 🥕
  
## Prérequis

- Python 3.x
- Pygame
- Numpy
- Noise (pour le bruit de Perlin)

Installez les dépendances si nécessaire :  
```bash
pip install -r requirements.txt
```

## Utilisation

1. Clonez ce dépôt :
   
2. Lancez le script principal :
    ```bash
    python main.py
    ```
   
3. Une fenêtre Pygame s'ouvre, affichant la carte de nutriments et les arbres. Les animaux se déplacent également.

4. **Interaction** :  
   - Cliquez sur un arbre (graine ou vivant) pour afficher ses informations dans la console.  
   - Observez le vieillissement des arbres, leur énergie, leur rayon, et la faim des animaux. 🧐

## Personnalisation

- Ajustez les paramètres du bruit pour modifier la distribution des nutriments.
- Modifiez les paramètres d'énergie, de croissance ou de faim pour changer la dynamique de l'écosystème.
- Ajoutez plus d'animaux, variez leur vitesse, leur rayon d'action ou leur stratégie de déplacement. 🦉

## Prochaines Étapes

- Implémenter davantage d'interactions : animaux herbivores, carnivores, arbres produisant des fruits, etc.
- Améliorer l'interface graphique.
- Ajouter une persistence des données et des statistiques. 📈

Bon voyage dans ce petit monde virtuel ! ✨
