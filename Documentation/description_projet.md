# Projet d'Optimisation - Le Voyageur de Commerce (TSP)

Ce document explique le but et le fonctionnement de ce projet.

## Objectif

L'objectif principal de ce projet est de résoudre le problème du Voyageur de Commerce (Traveling Salesperson Problem - TSP). Il s'agit de trouver le cycle hamiltonien de coût minimum dans un graphe complet pondéré, c'est-à-dire le chemin le plus court passant par toutes les villes une seule fois et revenant au point de départ.

Ce projet a été réalisé dans le cadre du Master MIASHS — IMA-UCO (2025–2026).

**Auteurs :**

- Matthias Jourdren
- Maxence Cornu Basset
- Gaëtan Pezas

## Méthodes Implémentées

Le projet compare quatre approches algorithmiques différentes pour résoudre le TSP :

1. **Méthode Exacte (Branch and Bound)**

   - Explore l'arbre des solutions possibles.
   - Garantit la solution optimale mais a une complexité factorielle $O(n!)$.
   - Utilise un mécanisme de "pruning" pour couper les branches qui ne peuvent pas améliorer la meilleure solution trouvée.

2. **Heuristique Constructive (Plus Proche Voisin)**

   - Construit une solution pas à pas en choisissant toujours la ville non visitée la plus proche.
   - Très rapide ($O(n^2)$) mais ne garantit pas l'optimalité.

3. **Recherche Locale (2-opt)**

   - Améliore une solution existante en effectuant des échanges d'arêtes (inversion de l'ordre de parcours entre deux villes) pour réduire la distance totale.
   - Permet de sortir de certains optima locaux.

4. **Méta-heuristique (GRASP)**

   - _Greedy Randomized Adaptive Search Procedure_.
   - Combine une phase de construction aléatoire (choix parmi les meilleurs candidats) et une phase de recherche locale (2-opt).
   - Répète le processus plusieurs fois pour trouver une solution robuste.

## Structure du Projet

- `src/` : Contient le code source des algorithmes (exact, constructive, local_search, grasp).
- `instances/` : Contient les jeux de données de test (fichiers `.in`).
- `LateX/` ou `report/` : Contient le rapport du projet.
- `results/` : Résultats des exécutions.

## Comment lancer le projet

Les différents algorithmes peuvent être lancés en ligne de commande depuis la racine du projet.

**Exemples :**

- **Exact :** `python3 src/exact/tsp_exact.py instances/exact/test.in`
- **Constructive :** `python3 src/constructive/tsp_constructive.py Data/17.in`
- **Local Search :** `python3 src/local_search/tsp_local_search.py Data/17.in`
- **GRASP :** `python3 src/grasp/tsp_grasp.py Data/17.in`

Pour lancer un benchmark complet sur plusieurs instances :
`python3 benchmark.py --instances Data --output results.csv --max-instances 5`
