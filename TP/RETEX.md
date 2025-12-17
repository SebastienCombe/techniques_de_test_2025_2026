# Retour d'Expérience - TP Triangulation

**Nom/Prénom :** Combe Sébastien

## 1. Contexte et Objectifs
L'objectif de ce TP était de concevoir un micro-service capable de réaliser une triangulation de polygones à partir d'un ensemble de points fournis par un service tiers (`PointSetManager`).
Les contraintes principales étaient :
- Une communication via API REST.
- Un format de données binaire (sérialisation custom).
- Une approche TDD (Test Driven Development) stricte.
- Une couverture de code de 100%.

## 2. Architecture et Choix Techniques

### Langage et Frameworks
J'ai choisi **Python** avec **Flask** pour sa simplicité.
- **Flask** : Pour exposer l'API REST `/triangulation/<id>`.
- **Struct** : Module standard Python utilisé pour gérer la conversion binaire (Little Endian).
- **Requests** : Pour la communication HTTP avec le `PointSetManager`.

### Algorithme
Pour la triangulation, j'ai implémenté une approche **"Naïve"** (ou triangulation en éventail) :
1. Tri des points selon l'axe X.
2. Utilisation du premier point comme pivot.
3. Connexion du pivot à toutes les paires de points suivants.

Bien que cette approche ne garantisse pas des triangles "équilibrés" (comme Delaunay), elle est suffisante pour valider le pipeline technique.

## 3. Méthodologie TDD

J'ai suivi l'approche **Test First** recommandée :
1. **Tests Unitaires** : J'ai d'abord écrit les tests pour le sérialiseur (`test_serializer.py`) avant d'implémenter la logique binaire.
2. **Mocking** : Pour l'API, j'ai utilisé `requests-mock` afin de simuler le `PointSetManager`. Cela m'a permis de développer sans avoir besoin de lancer le vrai service java à côté.
3. **Tests de Performance** : J'ai validé que le service tenait la charge (10 000 points en moins de 0.2s) grâce à un test dédié.

## 4. Difficultés Rencontrées et Solutions

### La gestion du Binaire
La manipulation d'octets avec `struct` et `bytearray` était la partie la plus délicate. Il fallait être rigoureux sur le calcul des offsets (4 octets pour les Header, 8 pour les Points).
*Solution :* J'ai beaucoup utilisé le debugger et décomposé le code en petites étapes (lecture header -> lecture boucle).

### Le Coverage (Les derniers %)
J'ai atteint rapidement 98% de couverture, mais les 2% restants étaient difficiles à obtenir.
Le problème venait d'un code "trop défensif" dans le sérialiseur : je vérifiais la taille des données avec des `if` avant de lire, ce qui rendait le bloc `except` final inaccessible (Code Mort).
*Solution :* J'ai ajouté un test spécifique envoyant un type invalide (`None`) pour forcer le passage dans le bloc `except` et atteindre les 100%.

## 5. Bilan
Ce projet m'a permis de comprendre l'importance de l'isolation dans les tests. Le fait de mocker les dépendances (API externe) rend les tests beaucoup plus rapides et fiables.
L'objectif de performance est largement atteint, et le code est entièrement couvert par les tests.