#!/bin/bash

# Script d'automatisation pour macOS/Linux

echo "========================================"
echo "      Lancement du Benchmark TSP"
echo "========================================"

# Lancer le benchmark
python3 benchmark.py

# Vérifier si le benchmark s'est bien passé
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Benchmark terminé avec succès."
    echo "----------------------------------------"
    echo "      Génération des graphiques..."
    echo "----------------------------------------"
    
    # Lancer la génération des courbes
    python3 plot_results.py

    echo "----------------------------------------"
    echo "      Compilation du rapport LaTeX..."
    echo "----------------------------------------"
    pdflatex LateX/report.tex
    
    echo ""
    echo "✅ Terminé ! Les résultats sont dans le dossier 'results' et le rapport est généré."
else
    echo ""
    echo "❌ Une erreur est survenue lors du benchmark."
    exit 1
fi
