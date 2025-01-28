#!/usr/bin/env python3
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List

def load_algorithm_results(results_dir: str) -> Dict[str, Dict[str, List]]:
    """
    Laad alle resultaten uit de experiments directory.
    
    Args:
        results_dir: Pad naar de results directory
        
    Returns:
        Dictionary met resultaten voor elk algoritme en dataset
    """
    all_results = {}
    
    # Loop door results directory
    for root, dirs, files in os.walk(results_dir):
        algorithm = os.path.basename(root)
        if algorithm not in all_results and algorithm != 'results':
            all_results[algorithm] = {'holland': [], 'national': []}
            
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    dataset = data['dataset']
                    results = [r['score'] for r in data['results'] if r['score'] is not None]
                    all_results[algorithm][dataset].extend(results)
    
    return all_results

def analyze_results(results: Dict[str, Dict[str, List]], visualization_dir: str):
    """
    Maak visualisaties en analyse van de resultaten.
    
    Args:
        results: Dictionary met resultaten voor elk algoritme en dataset
        visualization_dir: Directory om visualisaties op te slaan
    """
    # Zorg ervoor dat de visualization directory bestaat
    os.makedirs(visualization_dir, exist_ok=True)
    
    # Maak vergelijkingsplots voor elke dataset
    for dataset in ['holland', 'national']:
        # Maak boxplot
        plt.figure(figsize=(15, 8))
        data = []
        labels = []
        
        for algorithm in results:
            if results[algorithm][dataset]:
                data.append(results[algorithm][dataset])
                labels.append(algorithm)
        
        plt.boxplot(data, labels=labels)
        plt.title(f'Algoritme Prestatie Vergelijking - {dataset.upper()} Dataset')
        plt.ylabel('Kwaliteitsscore')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(visualization_dir, f'algorithm_comparison_{dataset}.png'))
        plt.close()
        
        # Maak statistieken tabel
        stats = {
            'Algoritme': [],
            'Gemiddelde Score': [],
            'Maximum Score': [],
            'Minimum Score': [],
            'Standaarddeviatie': []
        }
        
        for algorithm in results:
            if results[algorithm][dataset]:
                stats['Algoritme'].append(algorithm)
                scores = results[algorithm][dataset]
                stats['Gemiddelde Score'].append(f"{sum(scores)/len(scores):.2f}")
                stats['Maximum Score'].append(f"{max(scores):.2f}")
                stats['Minimum Score'].append(f"{min(scores):.2f}")
                stats['Standaarddeviatie'].append(f"{pd.Series(scores).std():.2f}")
        
        # Sla statistieken op in CSV
        stats_df = pd.DataFrame(stats)
        stats_df.to_csv(os.path.join(visualization_dir, f'algorithm_stats_{dataset}.csv'), 
                       index=False)

def main():
    # Verkrijg paden relatief aan dit script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    results_dir = os.path.join(current_dir, 'results')
    visualization_dir = os.path.join(project_root, 'visualization')
    
    # Laad en analyseer resultaten
    results = load_algorithm_results(results_dir)
    analyze_results(results, visualization_dir)
    
    print("Analyse voltooid. Bekijk de visualization directory voor resultaten.")

if __name__ == "__main__":
    main()