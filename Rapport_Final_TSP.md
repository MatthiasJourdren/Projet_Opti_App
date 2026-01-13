# Rapport de Projet : Problème du Voyageur de Commerce (TSP)

## 1. Introduction et Énoncé du Problème

Le Problème du Voyageur de Commerce (**Traveling Salesperson Problem - TSP**) est l'un des problèmes d'optimisation combinatoire les plus célèbres et les plus étudiés. 

### Énoncé
Étant donné un ensemble de villes et les distances entre chaque paire de villes, l'objectif est de trouver le chemin le plus court qui :
1. Visite chaque ville exactement une fois.
2. Revient à la ville de départ.

Mathématiquement, cela revient à chercher un **cycle hamiltonien de poids minimum** dans un graphe complet pondéré $G = (V, E)$. Le TSP est classé comme **NP-difficile**, ce qui signifie qu'il n'existe pas d'algorithme connu capable de trouver la solution optimale en temps polynomial pour toutes les instances.

---

## 2. Méthodes et Heuristiques Implémentées

### 2.1 Méthode Exacte : Branch and Bound

L'algorithme de séparation et d'évaluation (Branch and Bound) explore l'arbre des solutions possibles tout en utilisant des bornes pour ignorer les branches qui ne peuvent pas mener à une solution meilleure que celle déjà trouvée.

**Pseudo-code :**
```text
Fonction BranchAndBound(chemin_actuel, cout_actuel):
    Si cout_actuel >= meilleur_cout: 
        Retourner (Élagage)
        
    Si longueur(chemin_actuel) == N:
        cout_total = cout_actuel + distance(dernier, depart)
        Si cout_total < meilleur_cout:
            meilleur_cout = cout_total
            meilleur_chemin = copie(chemin_actuel)
        Retourner

    Pour chaque ville suivante non visitée:
        Marquer ville comme visitée
        BranchAndBound(chemin_actuel + ville, cout_actuel + distance(dernier, ville))
        Marquer ville comme non visitée
```

*   **Complexité :** $O(n!)$ dans le pire des cas. Bien que l'élagage réduise l'espace de recherche, le nombre de nœuds explorés croît de manière exponentielle avec $n$.

---

### 2.2 Heuristique Constructive : Plus Proche Voisin

C'est une approche gloutonne simple qui construit une solution en choisissant toujours la ville non visitée la plus proche du point actuel.

**Pseudo-code :**
```text
Fonction PlusProcheVoisin(G):
    Choisir ville_depart (ex: 0)
    ville_actuelle = ville_depart
    Marquer ville_actuelle comme visitée
    Tant qu'il reste des villes non visitées:
        Trouver ville_suivante non visitée la plus proche de ville_actuelle
        Ajouter ville_suivante au chemin
        cout_total += distance(ville_actuelle, ville_suivante)
        ville_actuelle = ville_suivante
    cout_total += distance(ville_actuelle, ville_depart)
    Retourner chemin, cout_total
```

*   **Complexité :** $O(n^2)$, car pour chaque ville ($n$), on parcourt les autres villes pour trouver la plus proche ($n$).

---

### 2.3 Recherche Locale : 2-opt

L'algorithme 2-opt tente d'améliorer une solution existante en inversant des segments du tour pour éliminer les croisements d'arêtes.

**Pseudo-code :**
```text
Fonction RechercheLocale2Opt(tour_initial):
    amélioration = Vrai
    Tant que amélioration:
        amélioration = Faux
        Pour i de 1 à N-2:
            Pour k de i+1 à N-1:
                nouveau_tour = InverserSegment(tour_initial, i, k)
                Si cout(nouveau_tour) < cout(tour_initial):
                    tour_initial = nouveau_tour
                    amélioration = Vrai
                    Sortir des boucles de parcours (First Improvement)
    Retourner tour_initial
```

*   **Complexité :** $O(n^2)$ par itération. Le nombre total d'itérations peut varier, mais chaque amélioration est coûteuse en calcul de distance.

---

### 2.4 Méta-heuristique : GRASP (Greedy Randomized Adaptive Search Procedure)

GRASP combine la construction aléatoire pour la diversité et la recherche locale pour la qualité.

**Pseudo-code :**
```text
Fonction GRASP(max_itérations, alpha):
    Pour i de 1 à max_itérations:
        // Phase 1 : Construction
        Solution = ConstructionAléatoireGourmande(alpha)
        // Phase 2 : Recherche Locale
        Solution = RechercheLocale2Opt(Solution)
        
        Si cout(Solution) < meilleur_cout_global:
            meilleur_Solution = Solution
    Retourner meilleur_Solution
```

*   **Complexité :** $O(I \times (n^2 + \text{itérations\_2opt}))$, où $I$ est le nombre d'itérations GRASP.

---

## 3. Résultats et Comparaison

Sur la base des benchmarks réalisés sur des instances de taille 20 :

| Algorithme | Status | Temps (s) | Coût (Moyen) | Qualité |
| :--- | :--- | :--- | :--- | :--- |
| **Exact (B&B)** | Timeout (>60s) | - | - | Optimale (si fini) |
| **Plus Proche Voisin**| Succès | ~0.03s | 100% (Base) | Faible |
| **Recherche Locale** | Succès | ~0.03s | ~95% | Moyenne |
| **GRASP** | Succès | ~0.12s | ~90% | **Excellente** |

### Analyse
1.  **Méthode Exacte** : Inutilisable au-delà de 15-20 villes en raison de l'explosion combinatoire.
2.  **Plus Proche Voisin** : Extrêmement rapide mais produit souvent des solutions de mauvaise qualité avec des "grands sauts" à la fin.
3.  **Local Search (2-opt)** : Améliore significativement la solution initiale pour un surcoût temporel négligeable.
4.  **GRASP** : Offre le meilleur compromis. En multipliant les points de départ (randomisation) et en les raffinant par 2-opt, il trouve des solutions bien meilleures que les méthodes simples en restant très rapide ( < 1 seconde).

---

## 4. Conclusion

L'heuristique retenue comme étant la plus efficace est **GRASP**. 

Bien qu'elle ne garantisse pas l'optimalité mathématique (contrairement au Branch and Bound), elle fournit des solutions de haute qualité en un temps de calcul très court, ce qui est crucial pour des applications réelles où le nombre de villes dépasse rapidement les capacités des méthodes exactes. Sa robustesse provient de sa capacité à explorer différentes zones de l'espace de recherche grâce à sa phase aléatoire, tout en exploitant les optima locaux via le 2-opt.