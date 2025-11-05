TP/
├── src/
│   ├── __init__.py
│   ├── app.py              
│   ├── core.py             
│   └── serializer.py       
├── tests/
│   ├── __init__.py
│   ├── conftest.py         
│   ├── unit/               
│   ├── component/          
│   └── performance/        
├── requirements.txt
├── dev_requirements.txt
├── pyproject.toml          
├── Makefile                
└── PLAN.md

# PLAN.md - Stratégie de Test pour le Micro-service Triangulator

## 1. Introduction
Ce document décrit la stratégie de validation du micro-service `Triangulator`. L'approche adoptée est le **Test-Driven Development (TDD)**. Nous définirons les tests avant l'implémentation pour garantir la conformité aux spécifications binaires et fonctionnelles.

## 2. Périmètre des Tests

Les tests sont divisés en trois catégories distinctes, pilotables via le `Makefile`.

### 2.1 Tests Unitaires (Focus : Logique interne)
Ces tests valident les fonctions pures, sans contexte HTTP ni dépendance externe.

* **Sérialisation / Désérialisation (Serializer)**
    * *Objectif :* Garantir que le format binaire propriétaire est respecté.
    * *Cas de test 1 :* Décodage d'un `PointSet` binaire valide (vérification du header, nombre de points, coordonnées float).
    * *Cas de test 2 :* Encodage d'un objet `Triangles` en binaire (vérification de la structure : PointSet header + Triangles header + indices).
    * *Cas de test 3 :* Gestion des erreurs (binaire malformé, taille de buffer incohérente).

* **Algorithme de Triangulation (Core)**
    * *Objectif :* Vérifier la justesse géométrique.
    * *Cas de test 1 (Basique) :* 3 points formant un triangle -> Retourne 1 triangle reliant les indices 0, 1, 2.
    * *Cas de test 2 (Carré) :* 4 points formant un carré -> Retourne 2 triangles.
    * *Cas de test 3 (Vide) :* Moins de 3 points -> Retourne 0 triangle ou une erreur gérée.

### 2.2 Tests de Composant / API (Focus : Intégration et HTTP)
Ces tests valident le comportement du serveur Flask et ses interactions avec le `PointSetManager`. Nous utiliserons le **Mocking** pour simuler le `PointSetManager`.

* **Endpoint `GET /triangulation/{id}`**
    * *Scénario Nominal :*
        1. Le client demande la triangulation de l'ID "123".
        2. Le test intercepte l'appel sortant vers `PointSetManager` et renvoie un binaire `PointSet` préfabriqué.
        3. Vérification que le Triangulator répond 200 OK avec le binaire `Triangles` correct.
    * *Scénario Erreur Dépendance :*
        1. Le `PointSetManager` simulé répond 404 (ID inconnu).
        2. Le Triangulator doit propager une erreur 404 ou 400 au client.
    * *Scénario Erreur Serveur :*
        1. Le `PointSetManager` est inaccessible (timeout).
        2. Le Triangulator doit répondre 502 ou 503.

### 2.3 Tests de Performance
Ces tests sont isolés car longs à exécuter.

* *Objectif :* Mesurer le temps de réponse pour de grands ensembles de points.
* *Scénario :* Génération aléatoire de 10 000 points, mesure du temps de sérialisation + calcul.

## 3. Outillage et Métriques

* **Framework :** `pytest` pour l'exécution.
* **Mocking :** `unittest.mock` ou `requests-mock` pour simuler le `PointSetManager`.
* **Couverture :** Objectif de 100% de couverture de lignes (`branch coverage`) vérifié par `coverage.py`.
* **Qualité :** Linting strict via `ruff` avant tout commit.

## 4. Stratégie d'Implémentation (Roadmap)
1.  Mise en place du squelette et des outils CI (Makefile).
2.  Écriture des tests unitaires pour le `Serializer` (binaire).
3.  Implémentation du `Serializer` pour faire passer les tests.
4.  Écriture des tests d'API (avec Mocks) et algorithmiques.
5.  Implémentation de l'API Flask et de l'algo de triangulation.