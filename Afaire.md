# Reste à faire pour le Projet Opti

Basé sur l'analyse du sujet et du code actuel.

## 1. Expérimentations & Réglage des Paramètres

- [ ] **Justifier les paramètres** : Mettre en place des expériences pour "prouver" que les valeurs choisies (ex: `alpha`, `iterations`) sont les meilleures.
- [x] **Automatisation** : Créer des scripts pour lancer les tests sur plusieurs instances et collecter les résultats (CSV/JSON).
- [ ] **Comparaisons** :
  - [ ] Temps d'exécution vs Complexité théorique.
  - [ ] Qualité de solution vs Taille d'entrée (et autres paramètres).
  - [ ] Comparaison entre les méthodes (Constructive vs Local Search vs GRASP-LS vs Exact).

## 2. Cas Pathologiques

- [x] **Identifier ou Créer** des instances où les heuristiques échouent ou donnent de mauvais résultats par rapport à l'optimal.
- [ ] Documenter ces cas et l'écart type d'erreur.

## 3. Rapport (Dossier `report/`)

Le rapport doit être en PDF (LaTeX recommandé) et inclure :

- [x] **Explications détaillées** des algorithmes (Pseudo-code, pas de copier-coller du code python).
- [x] **Calcul de complexité** théorique.
- [ ] **Résultats expérimentaux** : Graphiques et analyses.
- [ ] **Justifications** des choix d'implémentation et de paramètres.
- [ ] **Conclusion**.

## 4. Conformité pour le Rendu

- [ ] **Structure des dossiers** : Vérifier que le zip final respecte exactement la structure demandée :
  - `src/model`, `src/exact`, `src/constructive`, `src/local_search`, `src/grasp`.
  - **Note** : Le sujet mentionne `src/tabu_search` dans les instructions de rendu (page 3) mais demande d'implémenter `GRASP` (page 1). Il faudra probablement renommer le dossier `grasp` en `tabu_search` juste pour le rendu si on suit la lettre, ou (mieux) ajouter une note dans le README expliquant que c'est GRASP comme demandé en section 5.
- [ ] **Instances** : Fournir les instances de test (paramétrage + comparaison finale) dans le dossier `instances/`.
- [ ] **README.md** : Doit expliquer comment compiler/exécuter, l'organisation, etc. (Le README actuel est un bon début mais doit être complété).
