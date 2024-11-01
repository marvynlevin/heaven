# Équipe Heaven - Projet NSI T3

## Informations Équipe
- **Membres** :
  - LEVIN Marvyn
  - MORRETI Tony
  - COLIN Cédric
- **Classe** : T6
- **Langages Utilisés** :
  - Python 3.7.10 (Pygame, Maths, Random, Typing, Enum, Json)
  - Rust 1.67.1 (en cas de fonctionnalités avancées)

## Documents liés au projet
- [Cahier des charges-pdf](./docs/cahierDesChargesTerm.pdf)
- [Soutenance-pdf](./docs/projetHeaven.pdf) [Soutenance-pptx](./docs/projetHeaven.pptx)
- [Logos Team Heaven](./docs/logos/)

## Cahier des Charges

### 1. Présentation du Projet
- **But** : Concevoir un jeu vidéo fonctionnel en 2D de style rétro, immersif et narratif.
- **Moyens** : Utilisation des connaissances en programmation, détermination, et mise en place d'un planning.
- **Langages de Programmation** :
  - **Python** pour le développement principal.
  - **Rust** pour des fonctionnalités avancées éventuelles.

### 2. Types de Fichiers
- **Icônes** : Les icônes sont réalisées par Freepik, source : [Flaticon](https://www.flaticon.com).

### 3. Recherche Documentaire
- **Ressources** :
  - [Cours Pygame](https://www.pygame.org/docs/)
  - [Tutoriels Python Pygame](https://pythonprogramming.net/pygame-python-3/)
  - [Tiled Documentation](https://doc.mapeditor.org/en/stable/manual/index.html)
  
### 4. Répartition du Travail
- **Tony** :
  - Manipulation de Tiled
  - Création de la tileset et de la map
  - Aide avec Pygame
- **Marvyn** :
  - Manipulation de Pygame
  - Création de l'interface du menu
  - Développement de classes (personnages, etc.)
- **Cédric** :
  - Manipulation de Pygame
  - Création de l'interface principale
  - Développement de classes

### 5. Outils de Collaboration
- **Discord** : Pour les discussions et le partage de fichiers.
- **WhatsApp** : Pour la communication rapide.
- **Visual Studio Code (Live Share)** : Pour le travail collaboratif sur le code.
- **TeamViewer** : Pour accéder aux ordinateurs à distance.

## Fonctionnalités
- **Principes de Fonctionnement** :
  - Boucles de jeu pour gérer les événements.
  - Utilisation de delta pour les animations fluides.

## Tests
- **Méthodologie** :
  - Tests unitaires pour chaque fonction.
  - Tests d'intégration pour vérifier les interactions entre les fonctions.
  - Tests d'utilisation réelle pour les cas imprévus.

## Problèmes Rencontrés
- **Bugs Identifiés** :
  - Problèmes de chargement dans Tiled.
  - Synchronisation entre le joueur et la caméra.
  - Bugs d'affichage sous certaines conditions.

## Extensions Proposées
- Ajout de fonctionnalités, d'une cinématique et d'une interface utilisateur plus riche.

## Conclusion
- Ce projet a permis de renforcer nos compétences en programmation Python et en conception de jeux vidéo.

## Calendrier du Projet
- **Étape 1** : Choix du projet et validation.
- **Étape 2** : Premier bilan d'avancement.
- **Étape 3** : Deuxième bilan d'avancement.
- **Étape 4** : Présentation orale.

## Histoire
- **Synopsis** : Kady, une épéiste hors pair, lutte contre Myrtis pour la domination du monde.
- **Personnages Principaux** :
  - Kady
  - Gabriel
  - Eris
  - Myrtis

## Concept Graphique
- **Graphismes et Cartes** : ![Map](./map/start_map2.png) ![Personages](./assets/player/kady.png)

## Instructions de Lancement

### Prérequis
Pour exécuter ce projet, vous devez avoir **Python** et **Pygame** installés sur votre machine.

### Étapes d'installation

1. **Installer Python :**
   Sur Linux (Ubuntu/Debian), utilisez la commande :
   ```bash
   sudo apt-get install python3
   ```

2. **Installer Pygame :**
   Une fois Python installé, installez la bibliothèque Pygame avec :
   ```bash
   pip install pygame
   ```

3. **Lancer le jeu :**
   Une fois les installations terminées, exécutez le jeu avec la commande :
   ```bash
   python main.py
   ```
