# Projet TSP - Équipe 5

## Équipe

**Team 5** - Master MIASHS, IMA-UCO (2025-2026)

---

## 📁 Structure du Projet

```
.
├── README.md                    # Ce fichier
├── report/                      # Rapport du projet
│   ├── report_team_5.pdf       # Rapport final (35 pages)
│   └── sources/                # Sources LaTeX et figures
│       ├── report_team_5.tex
│       └── figures/
├── src/                        # Code source
│   ├── model/                  # Modèle de graphe et utilitaires partagés
│   ├── exact/                  # Algorithme exact (Branch and Bound)
│   ├── constructive/           # Heuristique constructive (Plus Proche Voisin)
│   ├── local_search/           # Recherche locale (2-opt)
│   └── grasp/                  # Méta-heuristique GRASP
└── instances/                  # Instances de test
    ├── exact/                  # Instances pour Branch and Bound
    ├── constructive/           # Instances pour heuristique constructive
    ├── local_search/           # Instances pour recherche locale
    ├── grasp/                  # Instances pour GRASP
    └── new_instances/          # Nouveau jeu d'instances pour comparaison finale
```

---

## 🚀 Utilisation

### Algorithme Exact (Branch and Bound)

```bash
python3 src/exact/tsp_exact.py instances/exact/17.in
```

**Note** : Limité aux instances ~ 20 villes.

### Heuristique Constructive (Plus Proche Voisin)

```bash
python3 src/constructive/tsp_constructive.py instances/constructive/17.in
```

### Recherche Locale (2-opt)

```bash
python3 src/local_search/tsp_local_search.py instances/local_search/17.in
```

### Méta-heuristique GRASP

```bash
python3 src/grasp/tsp_grasp_ls.py instances/grasp/17.in
```

### Exécution Automatisée (Benchmark)

Pour exécuter les 4 algorithmes sur plusieurs instances automatiquement :

```bash
python3 benchmark.py --instances Data --max-instances 5
```

**Options** :

- `--instances` : Dossier contenant les instances (par défaut : `instances/new_instances`)
- `--max-instances` : Nombre maximum d'instances à tester
- `--output` : Fichier CSV de sortie (par défaut : `results/results.csv`)

**Résultat** : Fichier CSV avec temps d'exécution et coûts pour chaque algorithme.

---

## 📥 Format d'Entrée

Les fichiers d'instance (`.in`) contiennent :

- Ligne 1 : `n` (nombre de villes)
- Lignes suivantes : Coordonnées `(x, y)` de chaque ville

Exemple (`17.in`) :

```
17
565.0 575.0
25.0 185.0
...
```

---

## 📤 Format de Sortie

Chaque algorithme génère un fichier `.out` dans le même dossier que l'instance d'entrée :

**Nom** : `{instance}_{algorithme}.out`

**Contenu** :

```
Tour: 0 -> 5 -> 12 -> ... -> 0
Cost: 2085.0
```

---

## 📊 Instances de Test

### Instances de Référence

- **`instances/new_instances/`** : Jeu d'instances pour comparaison finale
  - `17.in` : 17 villes (petite instance)
  - `51.in` : 51 villes (instance moyenne)
  - `52.in` : 52 villes (instance moyenne)
  - `439.in` : 439 villes (grande instance)

### Instances par Algorithme

Chaque algorithme possède son propre dossier d'instances de test dans `instances/`.

---

## 📈 Rapport

Le rapport complet (35 pages) est disponible dans `report/report_team_5.pdf`.

**Contenu** :

- Introduction et applications du TSP
- Description détaillée des 4 algorithmes (principe, pseudo-code, complexité, cas pathologiques)
- Méthodologie de test et génération des instances
- Analyse comparative des résultats
- Validation de la complexité théorique
- Tests sur grande instance (439 villes)
- Conclusions et recommandations

---

## 🛠️ Dépendances

**Python 3** requis.

Aucune dépendance externe pour les algorithmes principaux.

---

## 📝 Notes Importantes

### Performances

D'après les tests (voir rapport section 5) :

- **Branch and Bound** : Optimal jusqu'à ~20 villes. Retourne la meilleure solution trouvée sur timeout pour les plus grandes instances.
- **Constructive** : Très rapide (0.04s) mais écart 5-17% à l'optimal.
- **LocalSearch** : Excellent compromis (< 0.1s sur instances moyennes, quasi-optimal).
- **GRASP** : Meilleures solutions sur instances moyennes (51-52 villes).

Sur grande instance (439 villes) :

- **LocalSearch** : Extrêmement rapide (~2s) grâce au calcul incrémental.
- **GRASP** : Excellente qualité en un temps maîtrisé (~4-5 minutes pour 10 itérations).

---

## 👥 Auteurs

**Équipe 5** - Master MIASHS, IMA-UCO (2025-2026)

- Matthias Jourdren
- Maxence Cornu Basset
- Gaëtan Pezas

---

_Pour plus de détails, consultez le rapport complet : `report/report_team_5.pdf`_
